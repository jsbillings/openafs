# Openafs Spec $Revision$

#define afsvers 1.8.6pre3
%define afsvers 1.8.7
%define pkgvers 1.8.7
# for beta/rc releases make pkgrel 0.<tag>
# for real releases make pkgrel 1 (or more for extra releases)
#define pkgrel 0.pre3
%define pkgrel 1
%define kmod_name openafs
%define dkms_version %{version}-%{pkgrel}%{?dist}

# Define the location of your init.d directory
%define initdir /etc/rc.d/init.d

# Make sure RPM doesn't complain about installed but non-packaged files.
#define __check_files  %{nil}

Summary: OpenAFS distributed filesystem
Name: openafs
Version: %{pkgvers}
Release: %{pkgrel}%{?dist}
License: IBM Public License
URL: http://www.openafs.org
BuildRoot: %{_tmppath}/%{name}-%{version}-root
Packager: OpenAFS Gatekeepers <openafs-gatekeepers@openafs.org>
Group: Networking/Filesystems
BuildRequires: %{?kdepend:%{kdepend}, } ncurses-devel, flex, bison, automake, autoconf, libtool
%if 0%{?fedora} >= 15 || 0%{?rhel} >= 7
BuildRequires: systemd-units
%endif
%if 0%{?fedora} >= 15 || 0%{?rhel} >= 6
BuildRequires: perl-devel
%endif
BuildRequires: perl(ExtUtils::Embed)
BuildRequires: krb5-devel

ExclusiveArch: %{ix86} x86_64 aarch64

#    http://dl.openafs.org/dl/openafs/candidate/%{afsvers}/...
Source0: http://www.openafs.org/dl/openafs/%{afsvers}/openafs-%{afsvers}-src.tar.bz2
Source1: http://www.openafs.org/dl/openafs/%{afsvers}/openafs-%{afsvers}-doc.tar.bz2
Source3: openafs-client.service
%define srcdir openafs-%{afsvers}

Source10: http://www.openafs.org/dl/openafs/%{afsvers}/RELNOTES-%{afsvers}
Source11: http://www.openafs.org/dl/openafs/%{afsvers}/ChangeLog
Source20: https://www.central.org/dl/cellservdb/CellServDB.2018-05-14
# firewalld service devinitions
Source21: afs3-bos.xml
Source22: afs3-callback.xml
Source23: afs3-fileserver.xml
Source24: afs3-prserver.xml
Source25: afs3-rmtsys.xml
Source26: afs3-update.xml
Source27: afs3-vlserver.xml
Source28: afs3-volser.xml

# Local patches
# Add patch from upstream to address gcc-10 errors
Patch01:  0001-Avoid-duplicate-definitions-of-globals.patch

%description
The AFS distributed filesystem.  AFS is a distributed filesystem
allowing cross-platform sharing of files among multiple computers.
Facilities are provided for access control, authentication, backup and
administrative management.

This package provides common files shared across all the various
OpenAFS packages but are not necessarily tied to a client or server.


##############################################################################
#
# build the userspace side of things if so requested
#
##############################################################################
%package client
Requires: binutils, openafs = %{version}
%if 0%{?fedora} >= 15 || 0%{?rhel} >= 7
Requires: systemd-units
Requires(post): systemd-units, systemd-sysv
Requires(preun): systemd-units
Requires(postun): systemd-units
%endif
Requires: %{name}-kmod >= %{version}
Provides: %{name}-kmod-common = %{version}
Summary: OpenAFS Filesystem Client
Group: Networking/Filesystem

%description client
The AFS distributed filesystem.  AFS is a distributed filesystem
allowing cross-platform sharing of files among multiple computers.
Facilities are provided for access control, authentication, backup and
administrative management.

This package provides basic client support to mount and manipulate
AFS.

%package server
Requires: openafs = %{version}
Summary: OpenAFS Filesystem Server
Group: Networking/Filesystems
%if 0%{?fedora} >= 15 || 0%{?rhel} >= 7
Requires: systemd-units
Requires(post): systemd-units, systemd-sysv
Requires(preun): systemd-units
Requires(postun): systemd-units
%endif

%description server
The AFS distributed filesystem.  AFS is a distributed filesystem
allowing cross-platform sharing of files among multiple computers.
Facilities are provided for access control, authentication, backup and
administrative management.

This package provides basic server support to host files in an AFS
Cell.

%package authlibs
Summary: OpenAFS authentication shared libraries
Group: Networking/Filesystems

%description authlibs
The AFS distributed filesystem.  AFS is a distributed filesystem
allowing cross-platform sharing of files among multiple computers.
Facilities are provided for access control, authentication, backup and
administrative management.

This package provides a shared version of libafsrpc and libafsauthent. 
None of the programs included with OpenAFS currently use these shared 
libraries; however, third-party software that wishes to perform AFS 
authentication may link against them.

%package authlibs-devel
Requires: openafs-authlibs = %{version}-%{release}
Requires: openafs-devel = %{version}-%{release}
Summary: OpenAFS shared library development
Group: Development/Filesystems

%description authlibs-devel
The AFS distributed filesystem.  AFS is a distributed filesystem
allowing cross-platform sharing of files among multiple computers.
Facilities are provided for access control, authentication, backup and
administrative management.

This package includes the static versions of libafsrpc and 
libafsauthent, and symlinks required for building against the dynamic 
libraries.

%package devel
Summary: OpenAFS Development Libraries and Headers
Group: Development/Filesystems
Requires: openafs = %{version}-%{release}

%description devel
The AFS distributed filesystem.  AFS is a distributed filesystem
allowing cross-platform sharing of files among multiple computers.
Facilities are provided for access control, authentication, backup and
administrative management.

This package provides static development libraries and headers needed
to compile AFS applications.  Note: AFS currently does not provide
shared libraries.

%package docs
Summary: OpenAFS user and administrator documentation
Requires: openafs = %{version}-%{release}
Group: Networking/Filesystems

%description docs
The AFS distributed filesystem.  AFS is a distributed filesystem
allowing cross-platform sharing of files among multiple computers.
Facilities are provided for access control, authentication, backup and
administrative management.

This package provides HTML documentation for OpenAFS users and system
administrators.

%package krb5
Summary: OpenAFS programs to use with krb5
Requires: openafs = %{version}
Group: Networking/Filesystems
BuildRequires: krb5-devel

%description krb5
The AFS distributed filesystem.  AFS is a distributed filesystem
allowing cross-platform sharing of files among multiple computers.
Facilities are provided for access control, authentication, backup and
administrative management.

This package provides compatibility programs so you can use krb5
to authenticate to AFS services, instead of using the AFS homegrown
krb4 lookalike services.

%package compat
Summary: OpenAFS client compatibility symlinks
Requires: openafs = %{version}, openafs-client = %{version}
Group: Networking/Filesystems
Obsoletes: openafs-client-compat

%description compat
The AFS distributed filesystem.  AFS is a distributed filesystem
allowing cross-platform sharing of files among multiple computers.
Facilities are provided for access control, authentication, backup and
administrative management.

This package provides compatibility symlinks in /usr/afsws.  It is
completely optional, and is only necessary to support legacy
applications and scripts that hard-code the location of AFS client
programs.

%package transarc-client
Summary: OpenAFS client compatibility symlinks
Requires: openafs = %{version}, openafs-client = %{version}
Group: Networking/Filesystems

%description transarc-client
The AFS distributed filesystem.  AFS is a distributed filesystem
allowing cross-platform sharing of files among multiple computers.
Facilities are provided for access control, authentication, backup and
administrative management.

This package provides compatibility symlinks for Transarc paths.  It
is completely optional, and is only necessary to support legacy
applications and scripts that hard-code the location of AFS client
programs.

This package can cause problems on systems that already have
directories in place before the package is installed.

%package transarc-server
Summary: OpenAFS client compatibility symlinks
Requires: openafs = %{version}, openafs-server = %{version}
Group: Networking/Filesystems

%description transarc-server
The AFS distributed filesystem.  AFS is a distributed filesystem
allowing cross-platform sharing of files among multiple computers.
Facilities are provided for access control, authentication, backup and
administrative management.

This package provides compatibility symlinks for Transarc paths.  It
is completely optional, and is only necessary to support legacy
applications and scripts that hard-code the location of AFS client
programs.

%if 0%{?fedora} >= 15 || 0%{?rhel} >= 7
%package client-firewalld
Summary: OpenAFS server firewalld configuration for a client
Requires: openafs = %{version}, openafs-client = %{version}, firewalld-filesystem
Requires(post): firewalld-filesystem
Group: Networking/Filesystems

%description client-firewalld
The AFS distributed filesystem.  AFS is a distributed filesystem
allowing cross-platform sharing of files among multiple computers.
Facilities are provided for access control, authentication, backup and
administrative management.

This package provides the service definitions to use in a firewalld
setup for an OpenAFS client.

%package server-firewalld
Summary: OpenAFS server firewalld configuration for a server
Requires: openafs = %{version}, openafs-server = %{version}, firewalld-filesystem
Requires(post): firewalld-filesystem
Group: Networking/Filesystems

%description server-firewalld
The AFS distributed filesystem.  AFS is a distributed filesystem
allowing cross-platform sharing of files among multiple computers.
Facilities are provided for access control, authentication, backup and
administrative management.

This package provides the service definitions to use in a firewalld
setup for an OpenAFS server.
%endif

%package -n dkms-openafs
Summary:        DKMS-ready kernel source for AFS distributed filesystem
Group:          Development/Kernel
Provides:       openafs-kernel = %{version}
Provides:       openafs-kmod = %{version}
Requires(pre):  dkms
Requires(pre):  flex, bison, gcc, make
Requires(post): dkms
Requires:	openafs-client = %{version}

%description -n dkms-openafs
The AFS distributed filesystem.  AFS is a distributed filesystem
allowing cross-platform sharing of files among multiple computers.
Facilities are provided for access control, authentication, backup and
administrative management.

This package provides the source code to allow DKMS to build an
AFS kernel module.


##############################################################################
#
# PREP
#
##############################################################################

%prep
# Install OpenAFS src and doc
%setup -q -b 1 -n %{srcdir}

# Patching
%patch01 -p1 -b .gcc10fix

##############################################################################
#
# building
#
##############################################################################
%build
kv='26'
case %{_arch} in
       x86_64)                         sysname=amd64_linux${kv}        ;;
       alpha*)                         sysname=alpha_linux_${kv}       ;;
       i386|i486|i586|i686|athlon)     sysname=i386_linux${kv}         ;;
       aarch64)                        sysname=arm64_linux26           ;;
       *)                              sysname=%{_arch}_linux${kv}     ;;
esac
DESTDIR=$RPM_BUILD_ROOT; export DESTDIR
CFLAGS="$RPM_OPT_FLAGS"; export CFLAGS

KRB5_CONFIG="%{krb5config}"
export KRB5_CONFIG

#if [[ ! -f configure ]]; then
   echo %{afsvers} > .version
   sh regen.sh
#fi

# Fedora 23+ won't compile with the redhat-hardened-ld
%if 0%{?fedora} >= 23
LDFLAGS=$( echo %__global_ldflags | sed 's!-specs=/usr/lib/rpm/redhat/redhat-hardened-ld!!'); export LDFLAGS
%endif

%configure \
       --with-afs-sysname=${sysname} \
       --disable-strip-binaries \
       --disable-kernel-module \
       --enable-debug \
       --with-krb5 \
       --enable-bitmap-later \
       --enable-supergroups \
    || exit 1

make
#make -j16

# Build the libafs tree
make only_libafs_tree || exit 1

##############################################################################
#
# installation
#
##############################################################################
%install
make install DESTDIR=$RPM_BUILD_ROOT
export DONT_GPRINTIFY=1

kv='26'

case %{_arch} in
       x86_64)                         sysname=amd64_linux${kv}        ;;
       alpha*)                         sysname=alpha_linux_${kv}       ;;
       i386|i486|i586|i686|athlon)     sysname=i386_linux${kv}         ;;
       *)                              sysname=%{_arch}_linux${kv}     ;;
esac

# Fix the location of restorevol, since it should be available for
# any user in /usr/bin
#mv $RPM_BUILD_ROOT%{_prefix}/afs/bin/restorevol $RPM_BUILD_ROOT%{_bindir}/restorevol

# Copy root.client config files
mkdir -p $RPM_BUILD_ROOT/etc/openafs
mkdir -p $RPM_BUILD_ROOT/etc/sysconfig
mkdir -p $RPM_BUILD_ROOT%{initdir}
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/cache/openafs
install -m 755 src/packaging/RedHat/openafs.sysconfig $RPM_BUILD_ROOT/etc/sysconfig/openafs
%if 0%{?fedora} < 15 && 0%{?rhel} < 7
install -m 755 src/packaging/RedHat/openafs-client.init $RPM_BUILD_ROOT%{initdir}/openafs-client
install -m 755 src/packaging/RedHat/openafs-server.init $RPM_BUILD_ROOT%{initdir}/openafs-server
%else
mkdir -p $RPM_BUILD_ROOT%{_unitdir}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/modules
install -m 644 %{SOURCE3} $RPM_BUILD_ROOT%{_unitdir}/openafs-client.service
install -m 755 src/packaging/RedHat/openafs-client.modules $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/modules/openafs-client.modules
install -m 644 src/packaging/RedHat/openafs-server.service $RPM_BUILD_ROOT%{_unitdir}/openafs-server.service
%endif


#
# Install DOCUMENTATION
#

# Build the DOC directory
mkdir -p $RPM_BUILD_ROOT/$RPM_DOC_DIR/openafs-%{afsvers}
tar cf - -C doc LICENSE html pdf | \
    tar xf - -C $RPM_BUILD_ROOT/$RPM_DOC_DIR/openafs-%{afsvers}
install -m 644 %{SOURCE10} $RPM_BUILD_ROOT/$RPM_DOC_DIR/openafs-%{afsvers}
install -m 644 %{SOURCE11} $RPM_BUILD_ROOT/$RPM_DOC_DIR/openafs-%{afsvers}

# Copy the uninstalled krb5 files (or delete the unused krb5 files)
#mv $RPM_BUILD_ROOT%{_prefix}/afs/bin/asetkey $RPM_BUILD_ROOT%{_sbindir}/asetkey

# remove unused man pages
for x in afs_ftpd afs_inetd afs_login afs_rcp afs_rlogind afs_rsh \
    dkload knfs symlink symlink_list symlink_make \
    symlink_remove; do
	rm -f $RPM_BUILD_ROOT%{_mandir}/man1/${x}.1
done

#
# create filelist
#
grep -v "^#" >openafs-file-list <<EOF-openafs-file-list
%{_bindir}/afsmonitor
%{_bindir}/bos
%{_bindir}/fs
%{_bindir}/pagsh
%{_bindir}/pagsh.krb
%{_bindir}/pts
%{_bindir}/restorevol
%{_bindir}/scout
%{_bindir}/sys
%{_bindir}/tokens
%{_bindir}/tokens.krb
%{_bindir}/translate_et
%{_bindir}/xstat_cm_test
%{_bindir}/xstat_fs_test
%{_bindir}/udebug
%{_bindir}/unlog
%{_sbindir}/backup
%{_sbindir}/butc
%{_sbindir}/fms
%{_sbindir}/fstrace
%{_sbindir}/read_tape
%{_sbindir}/rxdebug
%{_sbindir}/uss
%{_sbindir}/vos
%{_sbindir}/vsys
EOF-openafs-file-list

# add man pages to the list
cat openafs-man1files \
        | ( while read x; do echo "%{_mandir}/man1/$x"; done ) \
        >>openafs-file-list
cat openafs-man5files \
        | ( while read x; do echo "%{_mandir}/man5/$x"; done ) \
        >>openafs-file-list
cat openafs-man8files \
        | ( while read x; do echo "%{_mandir}/man8/$x"; done ) \
        >>openafs-file-list

#
# Install compatiblity links
#
for d in bin:bin etc:sbin; do
  olddir=`echo $d | sed 's/:.*$//'`
  newdir=`echo $d | sed 's/^.*://'`
  mkdir -p $RPM_BUILD_ROOT%{_prefix}/afsws/$olddir
  for f in `cat openafs-file-list`; do
    if echo $f | grep -q /$newdir/; then
      fb=`basename $f`
      ln -sf %{_prefix}/$newdir/$fb $RPM_BUILD_ROOT%{_prefix}/afsws/$olddir/$fb
    fi
  done
done

#
# Install transarc links
#
## Client
mkdir $RPM_BUILD_ROOT%{_prefix}/vice
ln -s %{_sysconfdir}/openafs $RPM_BUILD_ROOT%{_prefix}/vice/etc
ln -s %{_localstatedir}/cache/openafs $RPM_BUILD_ROOT%{_prefix}/vice/cache

## Server
mkdir $RPM_BUILD_ROOT%{_prefix}/afs
ln -s %{_sysconfdir}/openafs/server $RPM_BUILD_ROOT%{_prefix}/afs/etc
ln -s %{_localstatedir}/openafs $RPM_BUILD_ROOT%{_prefix}/afs/local
ln -s %{_localstatedir}/openafs/db $RPM_BUILD_ROOT%{_prefix}/afs/db
ln -s %{_localstatedir}/openafs/logs $RPM_BUILD_ROOT%{_prefix}/afs/logs
ln -s %{_localstatedir}/openafs/backup $RPM_BUILD_ROOT%{_prefix}/afs/backup
mkdir $RPM_BUILD_ROOT%{_prefix}/afs/bin
### find all the executables in /usr/sbin
for f in `find $RPM_BUILD_ROOT%{_prefix}/sbin -executable`; do
    fb=`basename $f`
    ln -s %{_sbindir}/$fb $RPM_BUILD_ROOT%{_prefix}/afs/bin/$fb
done
### find all the executables in /usr/libexec/openafs
for f in `find $RPM_BUILD_ROOT%{_libexec}/openafs -executable`; do
    fb=`basename $f`
    ln -s %{_libexec}/openafs/$fb $RPM_BUILD_ROOT%{_prefix}/afs/bin/$fb
done


#
# Remove files we're not installing
#

# the rest are not needed.
for f in dlog dpass install knfs livesys ; do
  rm -f $RPM_BUILD_ROOT%{_bindir}/$f
done

# not supported on Linux or duplicated
for f in kdb rmtsysd kpwvalid ; do
  rm -f $RPM_BUILD_ROOT%{_sbindir}/$f
done

# remove man pages from programs deleted above
for f in 1/dlog 1/copyauth 1/dpass 1/livesys 8/rmtsysd 8/aklog_dynamic_auth 8/kdb 8/kpwvalid 8/xfs_size_check 1/package_test 5/package 8/package ; do
  rm -f $RPM_BUILD_ROOT%{_mandir}/man$f.*
done

#delete static libraries not in upstream package
rm -f $RPM_BUILD_ROOT%{_libdir}/libjuafs.a
rm -f $RPM_BUILD_ROOT%{_libdir}/libuafs.a

# Populate /etc/openafs
install -p -m 644 src/packaging/RedHat/openafs-ThisCell $RPM_BUILD_ROOT%{_sysconfdir}/openafs/ThisCell
install -p -m 644 %{SOURCE20} $RPM_BUILD_ROOT%{_sysconfdir}/openafs/CellServDB.dist
touch $RPM_BUILD_ROOT%{_sysconfdir}/openafs/CellServDB.local
install -p -m 644 src/packaging/RedHat/openafs-cacheinfo $RPM_BUILD_ROOT%{_sysconfdir}/openafs/cacheinfo

# Populate /etc/openafs/server
## Create empty files to be configured later
mkdir $RPM_BUILD_ROOT%{_sysconfdir}/openafs/server
touch $RPM_BUILD_ROOT%{_sysconfdir}/openafs/server/CellServDB
touch $RPM_BUILD_ROOT%{_sysconfdir}/openafs/server/ThisCell
touch $RPM_BUILD_ROOT%{_sysconfdir}/openafs/server/krb.conf
touch $RPM_BUILD_ROOT%{_sysconfdir}/openafs/server/UserList


# Fix systemd service unit which has transarc paths
## Fix location of environment file
sed -i 's!EnvironmentFile=-/etc/sysconfig/openafs!EnvironmentFile=-%{_sysconfdir}/sysconfig/openafs-server!g' $RPM_BUILD_ROOT%{_unitdir}/openafs-server.service
## Fix location of CellServDB
sed -i 's!/usr/vice/etc/CellServDB!%{_sysconfdir}/openafs/CellServDB!g' $RPM_BUILD_ROOT%{_unitdir}/openafs-client.service
## Fix the location of afsd
sed -i 's!/usr/vice/etc/afsd!%{_sbindir}/afsd!' $RPM_BUILD_ROOT%{_unitdir}/openafs-client.service
## Fix location of bosserver
sed -i 's!/usr/afs/bin/bosserver!%{_sbindir}/bosserver!' $RPM_BUILD_ROOT%{_unitdir}/openafs-server.service
## Fix cacheinfo to point at /var/cache/openafs
sed -i 's!/usr/vice/cache!%{_localstatedir}/cache/openafs!' $RPM_BUILD_ROOT%{_sysconfdir}/openafs/cacheinfo

# Set the executable bit on libraries in libdir, so rpmbuild knows to
# create "Provides" entries in the package metadata for the libraries
chmod +x $RPM_BUILD_ROOT%{_libdir}/*.so*

%if 0%{?fedora} >= 15 || 0%{?rhel} >= 7
# Set up firewalld files
install -d -m 755 %{buildroot}%{_prefix}/lib/firewalld/services
install -p -m 644 %SOURCE21 %{buildroot}%{_prefix}/lib/firewalld/services/afs3-bos.xml
install -p -m 644 %SOURCE22 %{buildroot}%{_prefix}/lib/firewalld/services/afs3-callback.xml
install -p -m 644 %SOURCE23 %{buildroot}%{_prefix}/lib/firewalld/services/afs3-fileserver.xml
install -p -m 644 %SOURCE24 %{buildroot}%{_prefix}/lib/firewalld/services/afs3-prserver.xml
install -p -m 644 %SOURCE25 %{buildroot}%{_prefix}/lib/firewalld/services/afs3-rmtsys.xml
install -p -m 644 %SOURCE26 %{buildroot}%{_prefix}/lib/firewalld/services/afs3-update.xml
install -p -m 644 %SOURCE27 %{buildroot}%{_prefix}/lib/firewalld/services/afs3-vlserver.xml
install -p -m 644 %SOURCE28 %{buildroot}%{_prefix}/lib/firewalld/services/afs3-volser.xml
%endif

#
# install dkms source
#
install -d -m 755 $RPM_BUILD_ROOT%{_prefix}/src
cp -a libafs_tree $RPM_BUILD_ROOT%{_prefix}/src/openafs-%{dkms_version}

cat > $RPM_BUILD_ROOT%{_prefix}/src/openafs-%{dkms_version}/dkms.conf <<"EOF"

PACKAGE_VERSION="%{dkms_version}"

# Items below here should not have to change with each driver version
PACKAGE_NAME="openafs"
MAKE[0]='./configure --with-linux-kernel-headers=${kernel_source_dir} --with-linux-kernel-packaging && make && mv src/libafs/MODLOAD-*/openafs.ko .'
CLEAN="if [ -e src/libafs/Makefile ]; then make -C src/libafs clean; else true; fi"

BUILT_MODULE_NAME[0]="openafs"
DEST_MODULE_LOCATION[0]="/extra/$PACKAGE_NAME/"
STRIP[0]=no
AUTOINSTALL=yes
NO_WEAK_MODULES="true"

EOF


##############################################################################
###
### clean
###
##############################################################################
%clean
rm -f openafs-file-list
[ "$RPM_BUILD_ROOT" != "/" -a "x%{debugspec}" != "x1" ] && \
	rm -fr $RPM_BUILD_ROOT

##############################################################################
###
### scripts
###
##############################################################################
%pretrans -p <lua> transarc-client
-- Moves an existing cache directory out of the way so symlink
-- can be created
path = "/usr/vice/cache"
st = posix.stat(path)
if st and st.type == "directory" then
  status = os.rename(path, path .. ".rpmmoved")
  if not status then
    suffix = 0
    while not status do
      suffix = suffix + 1
      status = os.rename(path .. ".rpmmoved", path .. ".rpmmoved." .. suffix)
    end
    os.rename(path, path .. ".rpmmoved")
  end
end

%post client
%if 0%{?fedora} < 15 && 0%{?rhel} < 7
chkconfig --add openafs-client
%else
if [ $1 -eq 1 ] ; then 
    # Initial installation 
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi
%endif
if [ ! -d /afs ]; then
	mkdir /afs
	chown root.root /afs
	chmod 0755 /afs
	[ -x /sbin/restorecon ] && /sbin/restorecon /afs
fi

# Create the CellServDB
[ -f %{_sysconfdir}/sysconfig/openafs/CellServDB.local ] || touch %{_sysconfdir}/openafs/CellServDB.local

( cd %{_sysconfdir}/openafs ; \
  cat CellServDB.local CellServDB.dist > CellServDB ; \
  chmod 644 CellServDB )


%post server
#on an upgrade, don't enable if we were disabled
%if 0%{?fedora} < 15 && 0%{?rhel} < 7
if [ $1 = 1 ] ; then
  chkconfig --add openafs-server
fi
%{initdir}/openafs-server condrestart

%post authlibs
/sbin/ldconfig

%postun authlibs
/sbin/ldconfig

%preun
if [ $1 = 0 ] ; then
	[ -d /afs ] && rmdir /afs
	:
fi

%preun client
%if 0%{?fedora} < 15 && 0%{?rhel} < 7
if [ $1 = 0 ] ; then
        %{initdir}/openafs-client stop
        chkconfig --del openafs-client
fi
%else
if [ $1 -eq 0 ] ; then
    	# Package removal, not upgrade
    	/bin/systemctl --no-reload disable openafs-client.service > /dev/null 2>&1 || :
    	/bin/systemctl stop openafs-client.service > /dev/null 2>&1 || :
fi
%endif

%preun server
%if 0%{?fedora} < 15 && 0%{?rhel} < 7
if [ $1 = 0 ] ; then
        %{initdir}/openafs-server stop
        chkconfig --del openafs-server
fi
%else
if [ $1 -eq 0 ] ; then
    	/bin/systemctl --no-reload disable openafs-server.service > /dev/null 2>&1 || :
    	/bin/systemctl stop openafs-server.service > /dev/null 2>&1 || :
fi
%endif

%if 0%{?fedora} >= 15 || 0%{?rhel} >= 7
%postun client
/bin/systemctl daemon-reload >/dev/null 2>&1 || :

%postun server
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
%endif

%endif


%if 0%{?fedora} >= 15 || 0%{?rhel} >= 7
%triggerun -- openafs-client < 1.6.0-1
# Save the current service runlevel info
# User must manually run systemd-sysv-convert --apply httpd
# to migrate them to systemd targets
/usr/bin/systemd-sysv-convert --save openafs-client >/dev/null 2>&1 ||:

# Run this because the SysV package being removed won't do it
/sbin/chkconfig --del openafs-client >/dev/null 2>&1 || :

%triggerun -- openafs-server < 1.6.0-1
# Save the current service runlevel info
# User must manually run systemd-sysv-convert --apply httpd
# to migrate them to systemd targets
/usr/bin/systemd-sysv-convert --save openafs-server >/dev/null 2>&1 ||:

# Run this because the SysV package being removed won't do it
/sbin/chkconfig --del openafs-server >/dev/null 2>&1 || :
%endif

%if 0%{?fedora} >= 15 || 0%{?rhel} >= 7
%post client-firewalld
%firewalld_reload

%post server-firewalld
%firewalld_reload
%endif

%post -n dkms-openafs
dkms add -m openafs -v %{dkms_version} --rpm_safe_upgrade
dkms build -m openafs -v %{dkms_version} --rpm_safe_upgrade
dkms install -m openafs -v %{dkms_version} --rpm_safe_upgrade

%preun -n dkms-openafs
dkms remove -m openafs -v %{dkms_version} --rpm_safe_upgrade --all ||:

##############################################################################
###
### file lists
###
##############################################################################
%files 
#-f openafs-file-list
%defattr(-,root,root)
%config(noreplace) /etc/sysconfig/openafs
%{_bindir}/afsmonitor
%{_bindir}/bos
%{_bindir}/fs
%{_bindir}/pagsh
%{_bindir}/pagsh.krb
%{_bindir}/pts
%{_bindir}/restorevol
%{_bindir}/scout
%{_bindir}/sys
%{_bindir}/tokens
%{_bindir}/tokens.krb
%{_bindir}/translate_et
%{_bindir}/xstat_cm_test
%{_bindir}/xstat_fs_test
%{_bindir}/udebug
%{_bindir}/unlog
%{_sbindir}/backup
%{_sbindir}/butc
%{_sbindir}/fms
%{_sbindir}/fstrace
%{_sbindir}/read_tape
%{_sbindir}/rxdebug
%{_sbindir}/uss
%{_sbindir}/vos
%{_sbindir}/vsys
%{_libdir}/librokenafs.so.*
%{_libdir}/libafshcrypto.so.*
%{_mandir}/man1/fs*.gz
%{_mandir}/man1/pts*.gz
%{_mandir}/man1/vos*.gz
%{_mandir}/man1/afs.1.gz
%{_mandir}/man1/afsmonitor.1.gz
%{_mandir}/man1/pagsh.1.gz
%{_mandir}/man1/pagsh.krb.1.gz
%{_mandir}/man1/rxdebug.1.gz
%{_mandir}/man1/restorevol.1.gz
%{_mandir}/man1/scout.1.gz
%{_mandir}/man1/tokens.1.gz
%{_mandir}/man1/tokens.krb.1.gz
%{_mandir}/man1/translate_et.1.gz
%{_mandir}/man1/xstat_cm_test.1.gz
%{_mandir}/man1/xstat_fs_test.1.gz
%{_mandir}/man5/afsmonitor.5.gz
%{_mandir}/man1/udebug.1.gz
%{_mandir}/man1/unlog.1.gz
%{_mandir}/man5/uss.5.gz
%{_mandir}/man5/uss_bulk.5.gz
%{_mandir}/man8/bos*
%{_mandir}/man8/fstrace*
%{_mandir}/man1/sys.1.gz
%{_mandir}/man8/backup*
%{_mandir}/man5/butc.5.gz
%{_mandir}/man5/butc_logs.5.gz
%{_mandir}/man8/butc.8.gz
%{_mandir}/man8/fms.8.gz
%{_mandir}/man8/read_tape.8.gz
%{_mandir}/man8/fssync-debug*
%{_mandir}/man8/uss*
%{_mandir}/man5/CellServDB.5.gz
%{_mandir}/man5/ThisCell.5.gz
%doc %{_docdir}/openafs-%{afsvers}/LICENSE

%files docs
%defattr(-,root,root)
%docdir %{_docdir}/openafs-%{afsvers}
%dir %{_docdir}/openafs-%{afsvers}
%{_docdir}/openafs-%{afsvers}/ChangeLog
%{_docdir}/openafs-%{afsvers}/RELNOTES-%{afsvers}
%{_docdir}/openafs-%{afsvers}/pdf

%files client
%defattr(-,root,root)
%dir %{_localstatedir}/cache/openafs
%{_sysconfdir}/openafs/CellServDB.dist
%ghost %{_sysconfdir}/openafs/CellServDB
%config(noreplace) %{_sysconfdir}/openafs/CellServDB.local
%config(noreplace) %{_sysconfdir}/openafs/ThisCell
%config(noreplace) %{_sysconfdir}/openafs/cacheinfo
%config(noreplace) %{_sysconfdir}/sysconfig/openafs
%{_bindir}/afsio
%{_bindir}/cmdebug
%{_bindir}/up
%{_sbindir}/afsd
%{_prefix}/share/openafs/C/afszcm.cat
%if 0%{?fedora} < 15 && 0%{?rhel} < 7
%{initdir}/openafs-client
%else
%{_unitdir}/openafs-client.service
%{_sysconfdir}/sysconfig/modules/openafs-client.modules
%endif
%{_mandir}/man1/cmdebug.*
%{_mandir}/man1/up.*
%{_mandir}/man5/afs.5.gz
%{_mandir}/man5/afs_cache.5.gz
%{_mandir}/man5/afs_volume_header.5.gz
%{_mandir}/man5/afszcm.cat.5.gz
%{_mandir}/man5/cacheinfo.*
%{_mandir}/man8/afsd.*
%{_mandir}/man8/vsys.*
%{_mandir}/man5/CellAlias.*

%files server
%defattr(-,root,root)
%dir %{_sysconfdir}/openafs/server
%config(noreplace) %{_sysconfdir}/openafs/server/CellServDB
%config(noreplace) %{_sysconfdir}/openafs/server/ThisCell
%config(noreplace) %{_sysconfdir}/openafs/server/UserList
%config(noreplace) %{_sysconfdir}/openafs/server/krb.conf
%ghost %config(noreplace) %{_sysconfdir}/openafs/BosConfig
%ghost %config(noreplace) %{_sysconfdir}/openafs/server/rxkad.keytab
%ghost %config(noreplace) %{_sysconfdir}/sysconfig/openafs-server
%{_bindir}/akeyconvert
%{_sbindir}/bosserver
%{_sbindir}/bos_util
%{_libexecdir}/openafs/buserver
%{_libexecdir}/openafs/dafileserver
%{_sbindir}/dafssync-debug
%{_libexecdir}/openafs/dasalvager
%{_libexecdir}/openafs/davolserver
%{_libexecdir}/openafs/fileserver
%{_sbindir}/fssync-debug
%{_sbindir}/pt_util
%{_libexecdir}/openafs/ptserver
%{_libexecdir}/openafs/salvager
%{_libexecdir}/openafs/salvageserver
%{_sbindir}/salvsync-debug
%{_sbindir}/state_analyzer
%{_libexecdir}/openafs/upclient
%{_libexecdir}/openafs/upserver
%{_libexecdir}/openafs/vlserver
%{_sbindir}/volinfo
%{_libexecdir}/openafs/volserver
%{_sbindir}/prdb_check
%{_sbindir}/vldb_check
%{_sbindir}/vldb_convert
%{_sbindir}/voldump
%{_sbindir}/volscan
%if 0%{?fedora} < 15 && 0%{?rhel} < 7
%{initdir}/openafs-server
%else
%{_unitdir}/openafs-server.service
%endif
%{_mandir}/man3/AFS::ukernel.*
%{_mandir}/man5/AuthLog.*
%{_mandir}/man5/BackupLog.*
%{_mandir}/man5/BosConfig.*
%{_mandir}/man5/BosLog.*
%{_mandir}/man5/FORCESALVAGE.*
%{_mandir}/man5/FileLog.*
%{_mandir}/man5/KeyFile.*
%{_mandir}/man5/KeyFileExt.*
%{_mandir}/man5/NetInfo.*
%{_mandir}/man5/NetRestrict.*
%{_mandir}/man5/NoAuth.*
%{_mandir}/man5/PtLog.*
%{_mandir}/man5/SALVAGE.fs.*
%{_mandir}/man5/SalvageLog.*
%{_mandir}/man5/sysid.*
%{_mandir}/man5/UserList.*
%{_mandir}/man5/VLLog.*
%{_mandir}/man5/VolserLog.*
%{_mandir}/man5/bdb.DB0.*
%{_mandir}/man5/fms.log.*
%{_mandir}/man5/krb.conf.*
%{_mandir}/man5/krb.excl.*
%{_mandir}/man5/prdb.DB0.*
%{_mandir}/man5/salvage.lock.*
%{_mandir}/man5/tapeconfig.*
%{_mandir}/man5/vldb.DB0.*
%{_mandir}/man8/akeyconvert.*
%{_mandir}/man8/buserver.*
%{_mandir}/man8/fileserver.*
%{_mandir}/man8/dafileserver.*
%{_mandir}/man8/dafssync-debug*
%{_mandir}/man8/dasalvager.*
%{_mandir}/man8/davolserver.*
%{_mandir}/man8/prdb_check.*
%{_mandir}/man8/ptserver.*
%{_mandir}/man8/pt_util.*
%{_mandir}/man8/salvager.*
%{_mandir}/man8/salvageserver.*
%{_mandir}/man8/state_analyzer.*
%{_mandir}/man8/upclient.*
%{_mandir}/man8/upserver.*
%{_mandir}/man8/vldb_check.*
%{_mandir}/man8/vldb_convert.*
%{_mandir}/man8/vlserver.*
%{_mandir}/man8/voldump.*
%{_mandir}/man8/volinfo.*
%{_mandir}/man8/volscan.*
%{_mandir}/man8/volserver.*

%files authlibs
%defattr(-,root,root)
%{_libdir}/libafsauthent.so.*
%{_libdir}/libafsrpc.so.*
%{_libdir}/libkopenafs.so.*

%files authlibs-devel
%defattr(-,root,root)
%{_includedir}/kopenafs.h
%{_libdir}/libafsauthent.a
%{_libdir}/libafscp.a
%{_libdir}/libafsrpc.a
%{_libdir}/libafsauthent_pic.a
%{_libdir}/libafsrpc_pic.a
%{_libdir}/libkopenafs.a
%{_libdir}/libafsauthent.so
%{_libdir}/libafsrpc.so
%{_libdir}/libkopenafs.so

%files devel
%defattr(-,root,root)
%{_bindir}/afs_compile_et
%{_bindir}/rxgen
%{_includedir}/afs
%{_includedir}/lock.h
%{_includedir}/lwp.h
%{_includedir}/rx
%{_includedir}/timer.h
%{_includedir}/ubik.h
%{_includedir}/ubik_int.h
%{_includedir}/opr/queue.h
%{_includedir}/opr/lock.h
%{_libdir}/afs
%{_libdir}/liblwp.a
%{_libdir}/libopr.a
%{_libdir}/librx.a
%{_libdir}/librxkad.a
%{_libdir}/librxstat.a
%{_libdir}/libubik.a
%{_libdir}/librokenafs.a
%{_libdir}/librokenafs.so
%{_libdir}/libafshcrypto.a
%{_libdir}/libafshcrypto.so
%{_libdir}/libafsrfc3961.a
%{_libdir}/libuafs_pic.a
%{_mandir}/man1/rxgen.*
%{_mandir}/man1/afs_compile_et.*

%files krb5
%defattr(-,root,root)
%{_bindir}/aklog
%{_bindir}/klog.krb5
%{_bindir}/asetkey
%{_mandir}/man1/aklog.*
%{_mandir}/man1/klog.krb5.1.gz
%{_mandir}/man8/asetkey.*

%files compat
%defattr(-,root,root)
%{_prefix}/afsws

%files transarc-client
%defattr(-,root,root)
%dir %{_prefix}/vice
%{_prefix}/vice/*
%ghost %{_prefix}/vice/cache.rpmmoved

%files transarc-server
%defattr(-,root,root)
%dir %{_prefix}/afs
%dir %{_prefix}/afs/bin
%{_prefix}/afs/bin/*
%{_prefix}/afs/backup
%{_prefix}/afs/etc
%{_prefix}/afs/db
%{_prefix}/afs/local
%{_prefix}/afs/logs

%if 0%{?fedora} >= 15 || 0%{?rhel} >= 7
%files client-firewalld
%defattr(-,root,root)
%{_prefix}/lib/firewalld/services/afs3-callback.xml
%{_prefix}/lib/firewalld/services/afs3-rmtsys.xml

%files server-firewalld
%defattr(-,root,root)
%{_prefix}/lib/firewalld/services/afs3-bos.xml
%{_prefix}/lib/firewalld/services/afs3-fileserver.xml
%{_prefix}/lib/firewalld/services/afs3-prserver.xml
%{_prefix}/lib/firewalld/services/afs3-update.xml
%{_prefix}/lib/firewalld/services/afs3-vlserver.xml
%{_prefix}/lib/firewalld/services/afs3-volser.xml
%endif

%files -n dkms-openafs
%defattr(-,root,root)
%{_prefix}/src/openafs-%{dkms_version}

##############################################################################
###
### openafs.spec change log
###
##############################################################################
%changelog
* Fri Jan 15 2021 Jonathan S. Billings <jsbillin@umich.edu> - 1.8.7-1
- Bump to 1.8.7
- Remove patch for rx-nextcid since it is included in this release

* Thu Jan 14 2021 Jonathan S. Billings <jsbillin@umich.edu> - 1.8.6-2
- Add Patches to fix rx-nextcid timestamp bug

* Thu Oct 24 2019 Jonathan S. Billings <jsbillin@umich.edu> - 1.8.5-1
- Bump to 1.8.5
- Addresses OPENAFS-SA-2019-001, OPENAFS-SA-2019-002 and OPENAFS-SA-2019-003

* Mon Oct 07 2019 Jonathan S. Billings <jsbillin@umich.edu> - 1.8.4-1
- Bump to 1.8.4

* Thu Sep 05 2019 Jonathan S. Billings <jsbillin@umich.edu> - 1.8.3-2
- Add patch to bump up the number of entries in a PTS group to 100k

* Wed Sep 04 2019 Jonathan S. Billings <jsbillin@umich.edu> - 1.8.3-1
- Bump to 1.8.3

* Wed Mar 20 2019 Jonathan S. Billings <jsbillin@umich.edu> - 1.8.3-0.pre1
- Packaged version 1.8.3pre1
- Add 'make' as a dependency for dkms-openafs

* Mon Feb 11 2019 Jonathan S. Billings <jsbillin@umich.edu> - 1.8.2-3
- Add firewalld subpackages to define service ports

* Wed Jan 23 2019 Jonathan S. Billings <jsbillin@umich.edu> - 1.8.2-2
- Add patches to address changes in linux 4.20 kernels
- rebuild autoconf due to patches

* Thu Sep 13 2018 Jonathan S. Billings <jsbillin@umich.edu> - 1.8.2-1
- Building 1.8.2
- Add patches to fix bugs introduced in OPENAFS-SA-2018-001 and
  OPENAFS-SA-2018-003, one of which led to compile errors.

* Fri Apr 13 2018 Jonathan S. Billings <jsbillin@umich.edu> - 1.8.0-1
- Building 1.8.0 final release

* Fri Jan 5 2018 Jonathan S. Billings <jsbillin@umich.edu> - 1.8.0-0.pre4
- Building 1.8.0 pre4

* Tue Dec 5 2017 Jonathan S. Billings <jsbillin@umich.edu> - 1.8.0-0.pre3
- Building 1.8.0 pre3

- Disable packaging of kaserver, pam_afs pam modules, kpasswd, man pages
* Wed Dec 14 2016 Jonathan S. Billings <jsbillin@umich.edu> - 1.8.0-0.pre1
- Building 1.8.0 pre1 alpha
- Disable packaging of kaserver, pam_afs pam modules, kpasswd, man pages
  and related software
- Include dkms package (from openafs-kmod spec file)
  
* Thu Dec 01 2016 Jonathan S. Billings <jsbillin@umich.edu> - 1.6.20-1
- Bumped to 1.6.20

* Mon Nov 14 2016 Jonathan S. Billings <jsbillin@umich.edu> - 1.6.19-1
- Bumped to 1.6.19

* Wed Jul 20 2016 Jonathan S. Billings <jsbillin@umich.edu> - 1.6.18.2-1
- Bumped to 1.6.18.2

* Mon May 9 2016 Jonathan S. Billings <jsbillin@umich.edu> - 1.6.18-1
- Bumped to 1.6.18

* Wed Mar 16 2016 Jonathan S. Billings <jsbillin@umich.edu> - 1.6.17-1
- Bumped to 1.6.17
- Changed systemd units from 0755 to 0644 permissions

* Thu Dec 17 2015 Jonathan S. Billings <jsbillin@umich.edu> - 1.6.16-1
- Bumped to 1.6.16

* Wed Oct 28 2015 Jonathan S. Billings <jsbillin@umich.edu> - 1.6.15-1
- Bumped to 1.6.15
- Addresses CVE-2015-7762 and CVE-2015-7763

* Thu Sep 24 2015 Jonathan S. Billings <jsbillin@umich.edu> - 1.6.14.1-2
- Ignore LD hardening added in Fedora 23

* Tue Sep 22 2015 Jonathan S. Billings <jsbillin@umich.edu> - 1.6.14.1-1
- Bumped to 1.6.14.1

* Mon Aug 17 2015 Jonathan S. Billings <jsbillin@umich.edu> - 1.6.14-1
- Bumped to 1.6.14

* Mon Jul 20 2015 Jonathan S. Billings <jsbillin@umich.edu> - 1.6.12-1.1
- Replace source tarballs with ones prepared by openafs.org

* Mon Jul 06 2015 Jonathan S. Billings <jsbillin@umich.edu> - 1.6.12-1
- rebuilt against 1.6.12

* Fri Jun 05 2015 Jonathan S. Billings <jsbillin@umich.edu> - 1.6.11.1-3
- Create an rpmtrans scriptlet to deal with a removing a directory where
  a symlink will eventually be created.

* Mon May 18 2015 Jonathan S. Billings <jsbillin@umich.edu> - 1.6.11.1-2
- Include our own openafs-client.service, which fixes several startup
  issues.

* Mon May 18 2015 Jonathan S. Billings <jsbillin@umich.edu> - 1.6.11.1-1
- rebuilt against 1.6.11.1

* Mon Mar 02 2015 Jonathan S. Billings <jsbillin@umich.edu> - 1.6.11-1
- rebuilt against 1.6.11

* Wed Oct  1 2014 Jonathan S. Billings <jsbillin@umich.edu> - 1.6.9-1
- Created initial spec file

