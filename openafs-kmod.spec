# Openafs Spec $Revision$
%define PACKAGE_VERSION 1.8.8
%define afsvers 1.8.8pre1
%define pkgrel 0.pre1.1
#define afsvers 1.8.7
#define pkgrel 3

Summary: OpenAFS distributed filesystem
Name: openafs-kmod
Version: %{PACKAGE_VERSION}
# Required for CentOS CBS, doesn't support release that has the date encoded
#Release: %{pkgrel}
# Encodes the date in the release, so you can rebuild it on a different day and get a different release (for new kernels)
Release: %{pkgrel}.%{expand:%(date +"%Y.%m.%d")}
License: IBM Public License
URL: http://www.openafs.org
BuildRoot: %{_tmppath}/%{name}-%{version}-root
Group: Networking/Filesystems
BuildRequires: flex, bison, automake, autoconf, krb5-devel, libtool, elfutils-libelf-devel

ExclusiveArch: %{ix86} x86_64 aarch64

Source0: http://www.openafs.org/dl/openafs/%{afsvers}/openafs-%{afsvers}-src.tar.bz2

Source10: http://www.openafs.org/dl/openafs/%{afsvers}/RELNOTES-%{afsvers}
Source11: http://www.openafs.org/dl/openafs/%{afsvers}/ChangeLog
Source13: find-installed-kversion.sh
Source14: openafs-kmodtool

# Local patches
## Fix for kernel panic caused by Crowdstrike
Patch00:  0001-afs-defer-afs_remunlink-when-task-fs-is-NULL.patch

%description
The AFS distributed filesystem.  AFS is a distributed filesystem
allowing cross-platform sharing of files among multiple computers.
Facilities are provided for access control, authentication, backup and
administrative management.

This package provides the kernel module for the OpenAFS client


%{expand:%(sh %{SOURCE13})}
%{expand:%(sh %{SOURCE14} rpmtemplate openafs %{kversion} /usr/sbin/depmod "")}

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
# Patches
%patch00 -p1 -b .afs-defer-afs_remunlink-when-task-fs-is-NULL

##############################################################################
#
# building
#
##############################################################################
%build
case %{_arch} in
       x86_64)                         sysname=amd64_linux26        ;;
       i386|i486|i586|i686|athlon)     sysname=i386_linux26         ;;
       aarch64)                        sysname=arm64_linux26        ;;
       *)                              sysname=%{_arch}_linux26     ;;
esac

# Otherwise, only regenerate if configure is missing
# if [[ ! -f configure ]]; then
    echo %{afsvers} > .version
    sh regen.sh
# fi

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
%files docs
%defattr(-,root,root)
%doc CODING CONTRIBUTING LICENSE README NEWS RELNOTES-%{afsvers} ChangeLog

##############################################################################
###
### openafs-kmod.spec change log
###
##############################################################################
%changelog
* Fri Jul 9 2021 Jonathan S. Billings <jsbillings@jsbillings.org> - 1.8.8-0.pre1.1
* Add patch to address kernel panic when running Crowdstrike
  (https://gerrit.openafs.org/14691)

* Mon Jun 14 2021 Jonathan S. Billings <jsbillings@jsbillings.org> - 1.8.8-0.pre1
* Build 1.8.8pre1 packages

* Tue May 25 2021 Jonathan S. Billings <jsbillings@jsbillings.org> - 1.8.7-3
- Add patch to let kernel module build for RHEL8.4
  (https://gerrit.openafs.org/#/c/14268/)

* Fri Jan 15 2021 Jonathan S. Billings <jsbillings@jsbillings.org> - 1.8.7-1
- Bump to 1.8.7
- Remove patch for rx-nextcid since it is included in this release

* Thu Jan 14 2021 Jonathan S. Billings <jsbillings@jsbillings.org> - 1.8.6-2
- Add Patches to fix rx-nextcid timestamp bug

* Mon Nov 09 2020 Jonathan S. Billings <jsbillings@jsbillings.org> - 1.8.6-1
- Bump to 1.8.6

* Thu Oct 24 2019 Jonathan S. Billings <jsbillings@jsbillings.org> - 1.8.5-1
- Bump to 1.8.5
- Addresses OPENAFS-SA-2019-001, OPENAFS-SA-2019-002 and OPENAFS-SA-2019-003

* Mon Oct 07 2019 Jonathan S. Billings <jsbillings@jsbillings.org> - 1.8.4-1
- Bump to 1.8.4

* Wed Mar 20 2019 Jonathan S. Billings <jsbillings@jsbillings.org> - 1.8.3-0pre1
- Building 1.8.3pre1

* Tue Dec 04 2018 Jonathan S. Billings <jsbillings@jsbillings.org> - 1.8.2-2
- Bumped release to make sure it is installed on RHEL/CentOS 7.6

* Thu Sep 13 2018 Jonathan S. Billings <jsbillings@jsbillings.org> - 1.8.2-1
- Building 1.8.2

* Mon Jun 04 2018 Jonathan S. Billings <jsbillings@jsbillings.org> - 1.8.0-2
- Adding patch from https://gerrit.openafs.org/#/c/13090/ to fix cache
  manager errors

* Fri Apr 13 2018 Jonathan S. Billings <jsbillings@jsbillings.org> - 1.8.0-1
- Building 1.8.0 final release

* Fri Jan 05 2018 Jonathan S. Billings <jsbillings@jsbillings.org> - 1.8.0-0.pre4
- Building 1.8.0 pre4

* Wed Dec 14 2016 Jonathan S. Billings <jsbillings@jsbillings.org> - 1.8.0-0.pre1
- Building 1.8.0 pre1 alpha
- Move dkms package into openafs spec file

* Thu Dec 01 2016 Jonathan S. Billings <jsbillings@jsbillings.org> - 1.6.20-1
- Bumped to 1.6.20

* Mon Nov 14 2016 Jonathan S. Billings <jsbillings@jsbillings.org> - 1.6.19-1
- Bumped to 1.6.19

* Wed Jul 20 2016 Jonathan S. Billings <jsbillings@jsbillings.org> - 1.6.18.2-1
- Bumped to 1.6.18.2

* Tue Jul 05 2016 Jonathan S. Billings <jsbillings@jsbillings.org> - 1.6.18.1-2
- Add patch for Fedora 24+ that fixes the PAGE_CACHE->PAGE rename.  See:
  https://github.com/torvalds/linux/commit/09cbfeaf1a5a67bfb3201e0c83c810cecb2efa5a

* Thu Jun 23 2016 Jonathan S. Billings <jsbillings@jsbillings.org> - 1.6.18.1-1
- Bumped to 1.6.18.1, which includes patches in previous release

* Mon Jun 20 2016 Jonathan S. Billings <jsbillings@jsbillings.org> - 1.6.18-4
- Add patches for 4.5+ kernels for f23+, rebased on
  openafs-stable-1_6_x branch

* Mon May 9 2016 Jonathan S. Billings <jsbillings@jsbillings.org> - 1.6.18-2
- Disable patch that can cause a deadlock, see
  https://gerrit.openafs.org/#/c/12267/

* Mon May 9 2016 Jonathan S. Billings <jsbillings@jsbillings.org> - 1.6.18-1
- Bumped to 1.6.18
- Also patch for 4.5 kernels in f24+

* Wed Mar 16 2016 Jonathan S. Billings <jsbillings@jsbillings.org> - 1.6.17-1
- Bumped to 1.6.17
- Also patch for 4.4 kernels in f22

* Thu Mar 10 2016 Jonathan S. Billings <jsbillings@jsbillings.org> - 1.6.16-2
- Added patches to allow OpenAFS to compile on 4.4 kernel, patches only
  applied for f23 or greater
- Added patch to disable use of splice() function for 4.4 kernel, only
  applied for f23 or greater

* Thu Dec 17 2015 Jonathan S. Billings <jsbillings@jsbillings.org> - 1.6.16-1
- Bumped to 1.6.16

* Wed Oct 28 2015 Jonathan S. Billings <jsbillings@jsbillings.org> - 1.6.15-1
- Bumped to 1.6.15
- Addresses CVE-2015-7762 and CVE-2015-7763

* Tue Sep 22 2015 Jonathan S. Billings <jsbillings@jsbillings.org> - 1.6.14.1-1
- Bumped to 1.6.14.1

* Mon Aug 17 2015 Jonathan S. Billings <jsbillings@jsbillings.org> - 1.6.14-1
- Bumped to 1.6.14

* Mon Jul 20 2015 Jonathan S. Billings <jsbillings@jsbillings.org> - 1.6.12-2
- Replace source tarballs with ones prepared by openafs.org

* Mon Jul 06 2015 Jonathan S. Billings <jsbillings@jsbillings.org> - 1.6.12-1
- Rebuilt for 1.6.12

* Mon May 18 2015 Jonathan S. Billings <jsbillings@jsbillings.org> - 1.6.11.1-1
- Rebuilt for 1.6.11.1

* Mon Mar 02 2015 Jonathan S. Billings <jsbillings@jsbillings.org> - 1.6.11-1.1
- Rebuilt for 1.6.11

* Wed Oct  1 2014 Jonathan S. Billings <jsbillings@jsbillings.org> - 1.6.9-1
- Created initial spec file

