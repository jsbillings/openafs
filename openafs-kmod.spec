# Openafs Spec $Revision$
%define pkgrel 1
%define afsvers 1.6.22
%define PACKAGE_VERSION 1.6.22

Summary: OpenAFS distributed filesystem
Name: openafs-kmod
Version: %{afsvers}
#Release: %{pkgrel}
Release: %{pkgrel}.%{expand:%(date +"%Y.%m.%d")}
License: IBM Public License
URL: http://www.openafs.org
BuildRoot: %{_tmppath}/%{name}-%{version}-root
Group: Networking/Filesystems
BuildRequires: pam-devel, flex, bison, automake, autoconf, elfutils-libelf-devel

ExclusiveArch: %{ix86} x86_64

Source0: http://www.openafs.org/dl/openafs/%{afsvers}/openafs-%{afsvers}-src.tar.bz2

Source10: http://www.openafs.org/dl/openafs/%{afsvers}/RELNOTES-%{afsvers}
Source11: http://www.openafs.org/dl/openafs/%{afsvers}/ChangeLog
Source13: find-installed-kversion.sh
Source14: openafs-kmodtool

# Patches
## Patch to prevent getcwd() ENOENT after shakeloose
## See: https://gerrit.openafs.org/#/c/12796/
Patch00:  prevent-getcwd-ENOENT-after-shakeloose.patch

%description
The AFS distributed filesystem.  AFS is a distributed filesystem
allowing cross-platform sharing of files among multiple computers.
Facilities are provided for access control, authentication, backup and
administrative management.

This package provides the kernel module for the OpenAFS client

%define dkms_version %{version}-%{pkgrel}%{?dist}
%{expand:%(sh %{SOURCE13})}
%{expand:%(sh %{SOURCE14} rpmtemplate openafs %{kversion} /usr/sbin/depmod "")}

%package -n dkms-openafs
Summary:        DKMS-ready kernel source for AFS distributed filesystem
Group:          Development/Kernel
Provides:       openafs-kernel = %{version}
Provides:       openafs-kmod = %{version}
Requires(pre):  dkms
Requires(pre):  flex, bison, gcc
Requires(post): dkms
Requires:	openafs-kmod-common = %{version}

%description -n dkms-openafs
The AFS distributed filesystem.  AFS is a distributed filesystem
allowing cross-platform sharing of files among multiple computers.
Facilities are provided for access control, authentication, backup and
administrative management.

This package provides the source code to allow DKMS to build an
AFS kernel module.

%package docs
Summary:        OpenAFS kernel module documentation
Group:          Networking/Filesystems
Requires:	openafs-kmod-common = %{version}

%description docs
The AFS distributed filesystem.  AFS is a distributed filesystem
allowing cross-platform sharing of files among multiple computers.
Facilities are provided for access control, authentication, backup and
administrative management.

This package provides the documentation for the AFS kernel module.


##############################################################################
#
# PREP
#
##############################################################################

%prep
# Just for logging purposes
echo '%kversion'
# Install OpenAFS src and doc
%setup -q -n openafs-%{afsvers}

# Patching
%if 0%{?rhel} == 7
%patch00 -p1 -b .prevent-getcwd-enoent
%endif

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

# Otherwise, only regenerate if configure is missing
 if [[ ! -f configure ]]; then
    sh regen.sh
 fi

./configure --with-afs-sysname=${sysname} \
  	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--bindir=%{_bindir} \
	--sbindir=%{_sbindir} \
        --with-linux-kernel-packaging \
	--with-linux-kernel-headers=/usr/src/kernels/%{kversion}.%{_target_cpu} \
	|| exit 1

make dest_only_libafs MPS=SP

# Build the libafs tree
make only_libafs_tree || exit 1


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
CLEAN="make -C src/libafs clean"

BUILT_MODULE_NAME[0]="openafs"
DEST_MODULE_LOCATION[0]="/extra/openafs/"
STRIP[0]=no
AUTOINSTALL=yes

EOF

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
### scripts
###
##############################################################################
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
%files docs
%defattr(-,root,root)
%doc src/LICENSE README README.DEVEL README.GIT NEWS RELNOTES-%{afsvers} ChangeLog

%files -n dkms-openafs
%defattr(-,root,root)
%{_prefix}/src/openafs-%{dkms_version}

##############################################################################
###
### openafs-kmod.spec change log
###
##############################################################################
%changelog
* Tue Dec 5 2017 Jonathan S. Billings <jsbillin@umich.edu> - 1.6.22-1
- Bumped to 1.6.22

* Mon Dec 4 2017 Jonathan S. Billings <jsbillin@umich.edu> - 1.6.21.1-2
- Added patch from https://gerrit.openafs.org/#/c/12796/ which prevents
  getcwd() ENOENT after shakeloose
- Bumped to 1.6.21.1

* Tue Jul 11 2017 Jonathan S. Billings <jsbillin@umich.edu> - 1.6.21-1
- Bumped to 1.6.21

* Thu Jun 1 2017 Jonathan S. Billings <jsbillin@umich.edu> - 1.6.20.2-2
- Added workaround to gcc7 bug in ./configure conftest

* Fri Apr 14 2017 Jonathan S. Billings <jsbillin@umich.edu> - 1.6.20.2-1
- Bumped to 1.6.20.2

* Thu Dec 01 2016 Jonathan S. Billings <jsbillin@umich.edu> - 1.6.20-1
- Bumped to 1.6.20

* Mon Nov 14 2016 Jonathan S. Billings <jsbillin@umich.edu> - 1.6.19-1
- Bumped to 1.6.19

* Wed Jul 20 2016 Jonathan S. Billings <jsbillin@umich.edu> - 1.6.18.2-1
- Bumped to 1.6.18.2

* Tue Jul 05 2016 Jonathan S. Billings <jsbillin@umich.edu> - 1.6.18.1-2
- Add patch for Fedora 24+ that fixes the PAGE_CACHE->PAGE rename.  See:
  https://github.com/torvalds/linux/commit/09cbfeaf1a5a67bfb3201e0c83c810cecb2efa5a

* Thu Jun 23 2016 Jonathan S. Billings <jsbillin@umich.edu> - 1.6.18.1-1
- Bumped to 1.6.18.1, which includes patches in previous release

* Mon Jun 20 2016 Jonathan S. Billings <jsbillin@umich.edu> - 1.6.18-4
- Add patches for 4.5+ kernels for f23+, rebased on
  openafs-stable-1_6_x branch

* Mon May 9 2016 Jonathan S. Billings <jsbillin@umich.edu> - 1.6.18-2
- Disable patch that can cause a deadlock, see
  https://gerrit.openafs.org/#/c/12267/

* Mon May 9 2016 Jonathan S. Billings <jsbillin@umich.edu> - 1.6.18-1
- Bumped to 1.6.18
- Also patch for 4.5 kernels in f24+

* Wed Mar 16 2016 Jonathan S. Billings <jsbillin@umich.edu> - 1.6.17-1
- Bumped to 1.6.17
- Also patch for 4.4 kernels in f22

* Thu Mar 10 2016 Jonathan S. Billings <jsbillin@umich.edu> - 1.6.16-2
- Added patches to allow OpenAFS to compile on 4.4 kernel, patches only
  applied for f23 or greater
- Added patch to disable use of splice() function for 4.4 kernel, only
  applied for f23 or greater

* Thu Dec 17 2015 Jonathan S. Billings <jsbillin@umich.edu> - 1.6.16-1
- Bumped to 1.6.16

* Wed Oct 28 2015 Jonathan S. Billings <jsbillin@umich.edu> - 1.6.15-1
- Bumped to 1.6.15
- Addresses CVE-2015-7762 and CVE-2015-7763

* Tue Sep 22 2015 Jonathan S. Billings <jsbillin@umich.edu> - 1.6.14.1-1
- Bumped to 1.6.14.1

* Mon Aug 17 2015 Jonathan S. Billings <jsbillin@umich.edu> - 1.6.14-1
- Bumped to 1.6.14

* Mon Jul 20 2015 Jonathan S. Billings <jsbillin@umich.edu> - 1.6.12-2
- Replace source tarballs with ones prepared by openafs.org

* Mon Jul 06 2015 Jonathan S. Billings <jsbillin@umich.edu> - 1.6.12-1
- Rebuilt for 1.6.12

* Mon May 18 2015 Jonathan S. Billings <jsbillin@umich.edu> - 1.6.11.1-1
- Rebuilt for 1.6.11.1

* Mon Mar 02 2015 Jonathan S. Billings <jsbillin@umich.edu> - 1.6.11-1.1
- Rebuilt for 1.6.11

* Wed Oct  1 2014 Jonathan S. Billings <jsbillin@umich.edu> - 1.6.9-1
- Created initial spec file

