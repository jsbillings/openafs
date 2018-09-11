#!/bin/bash

#if [[ -x /usr/bin/rpm ]] && /usr/bin/rpm --quiet -q kernel-headers; then
#        exec /usr/bin/rpm -q --qf '%%define kversion %{version}-%{release}\n' kernel-headers
#else

KVERSIONSTR=$(grep LINUX_VERSION_CODE /usr/include/linux/version.h)
KVERSIONNO=${KVERSIONSTR##* }
KVERSION1=$(( $KVERSIONNO >> 16 ))
KVERSION1R=$(( $KVERSIONNO - ( $KVERSION1 << 16 ) ))
KVERSION2=$(( $KVERSION1R >> 8 ))
KVERSION3=$(( $KVERSION1R - ( $KVERSION2 << 8 ) ))

if grep -q RHEL_RELEASE /usr/include/linux/version.h; then
        RVERSION=$(grep 'RHEL_RELEASE ' /usr/include/linux/version.h | cut -d'"' -f2)
        RHELMAJORSTR=$(grep RHEL_MAJOR /usr/include/linux/version.h)
        RHELMAJOR=el${RHELMAJORSTR##* }
else # assume fedora
        RHELMAJOR=fc$(cut -d' ' -f3 /etc/fedora-release)
        HRELEASE=$(rpm -q --qf "%{release}" kernel-headers | cut -d . -f1)
        if [[ "$HRELEASE" == "1" ]]; then
                # Last resort, use dnf
                RVERSION=$(dnf -q repoquery -C kernel-devel --qf "%{release}" | tail -1 | cut -d. -f1)
                
        else
                RVERSION=$HRELEASE
        fi
fi

printf "%%define kversion %d.%d.%d-%s.%s\n" $KVERSION1 $KVERSION2 $KVERSION3 $RVERSION $RHELMAJOR

#fi
