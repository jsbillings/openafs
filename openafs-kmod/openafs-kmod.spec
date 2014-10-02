# Openafs Spec $Revision$

Summary: OpenAFS distributed filesystem
Name: openafs-kmod
Version: 1.6.9
Release: 1%{?dist}
License: IBM Public License
URL: http://www.openafs.org
BuildRoot: %{_tmppath}/%{name}-%{version}-root
Group: Networking/Filesystems
BuildRequires: kernel, kernel-devel, pam-devel, flex, bison

ExclusiveArch: %{ix86} x86_64

Source0: http://www.openafs.org/dl/openafs/%{version}/openafs-%{version}-src.tar.bz2

Source10: http://www.openafs.org/dl/openafs/%{version}/RELNOTES-%{version}
Source11: http://www.openafs.org/dl/openafs/%{version}/ChangeLog
Source13: find-installed-kversion.sh

%description
The AFS distributed filesystem.  AFS is a distributed filesystem
allowing cross-platform sharing of files among multiple computers.
Facilities are provided for access control, authentication, backup and
administrative management.

This package provides the kernel module for the OpenAFS client

%{expand:%(sh %{SOURCE13})}
%{expand:%(sh /usr/lib/rpm/redhat/kmodtool rpmtemplate openafs %{kversion} "")}


##############################################################################
#
# PREP
#
##############################################################################

%prep
# Just for logging purposes
echo '%kversion'
# Install OpenAFS src and doc
%setup -q -n openafs-%{version}

##############################################################################
#
# building
#
##############################################################################
%build
case %{_arch} in
       x86_64)                         sysname=amd64_linux26        ;;
       i386|i486|i586|i686|athlon)     sysname=i386_linux26         ;;
       *)                              sysname=%{_arch}_linux26     ;;
esac

./configure --with-afs-sysname=${sysname} \
  	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--bindir=%{_bindir} \
	--sbindir=%{_sbindir} \
        --with-linux-kernel-packaging \
	--with-linux-kernel-headers=/usr/src/kernels/%{kversion}.%{_target_cpu} \
	|| exit 1

make dest_only_libafs MPS=SP

##############################################################################
#
# installation
#
##############################################################################
%install
case %{_arch} in
       x86_64)                         sysname=amd64_linux26        ;;
       i386|i486|i586|i686|athlon)     sysname=i386_linux26         ;;
       *)                              sysname=%{_arch}_linux26     ;;
esac

srcdir=${sysname}/dest/root.client/lib/modules/%{kversion}.%{_target_cpu}/extra/openafs
dstdir=$RPM_BUILD_ROOT/lib/modules/%{kversion}.%{_target_cpu}/extra/openafs

[ $RPM_BUILD_ROOT != / ] && rm -rf $RPM_BUILD_ROOT
install -D -m 755 ${srcdir}/openafs.ko ${dstdir}/openafs.ko

# copy Release notes and changelog into src dir
cp %{SOURCE10} %{SOURCE11} .

##############################################################################
###
### clean
###
##############################################################################
%clean
[ "$RPM_BUILD_ROOT" != "/" ] && \
	rm -fr $RPM_BUILD_ROOT

##############################################################################
###
### file lists
###
##############################################################################
%files
%defattr(-,root,root)
%doc src/LICENSE README README.DEVEL README.GIT NEWS RELNOTES-%{version} ChangeLog

##############################################################################
###
### openafs.spec change log
###
##############################################################################
%changelog
* Wed Oct  1 2014 Jonathan S. Billings <jsbillin@umich.edu> - 1.6.9-1
- Created initial spec file

