%global __os_install_post %{nil}

%define debug_package %{nil}

Name:           python-rpm-legacypython
Version:        4.12.0.2
Release:        72
License:        LGPL-2.1
Summary:        The RPM package management system
Url:            http://rpm.org/
Group:          base
Source0:        http://rpm.org/releases/rpm-4.12.x/rpm-4.12.0.2.tar.bz2
Patch0:         0001-Explicitly-set-beecrypt-include-directory.patch
Patch1:         0002-Ensure-lib-is-used-and-not-lib64.patch
Patch2:         0003-debuginfo-do-not-strip-static-libraries.patch
Patch5:         0006-Fix-32bit-kernel-builds-by-not-using-eu-strip.patch
Patch6:         0007-scripts-Don-t-bail-out-when-debugedit-fails.patch
Patch7:         0001-fileattrs-Ensure-we-match-all-binaries-for-elf-depen.patch
Patch8:         0008-build-id-non-fatal.patch
Patch9:         ldconfig-posttrans.patch
Patch10:        minidebuginfo.patch
Patch11:        nopyo.patch
patch12:        lib32.patch
patch13:        py3.patch
Patch14:        preserve-timestamp.patch
Patch15:        nofdatasync.patch
Patch16:        build-with-localhost-hostname.patch
Patch17:        0001-Add-RPMCALLBACK_ELEM_PROGRESS-callback-type.patch
Patch18:        0002-Move-RPMCALLBACK_ELEM_PROGRESS-to-rpmteProcess-to-ha.patch
Patch19:	fflush.patch

BuildRequires:  bzip2-dev
BuildRequires:  db-dev
BuildRequires:  elfutils-dev
BuildRequires:  file-dev
BuildRequires:  acl-dev
BuildRequires:  attr-dev
BuildRequires:  nss-dev nspr-dev
BuildRequires:  libstdc++-dev
BuildRequires:  openssl-dev
BuildRequires:  python-modules
BuildRequires:  xz-dev
BuildRequires:  pkgconfig(libpcre)
BuildRequires:  popt-dev
BuildRequires:	gettext 
BuildRequires:  automake automake-dev
BuildRequires:  libtool-dev
BuildRequires:  pkgconfig(python2)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(libarchive)
BuildRequires:  libtool autoconf m4 gettext-dev autoconf pkg-config-dev
BuildRequires:	bison flex
BuildRequires:  python3-dev

Requires: zip unzip


%description
The RPM package management system.

%prep
%setup -q -n rpm-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
# %patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1

%build
export PYTHON=/usr/bin/python2
autoreconf -fi
%configure \
 --sysconfdir=%{_sysconfdir} \
 --localstatedir=%{_localstatedir} \
 --with-external-db \
 --with-acl \
 --program-prefix= \
 --enable-nls \
 --without-beecrypt \
 --without-internal-beecrypt \
 --without-lua \
 --enable-python \
 --without-selinux \
 --libdir=/usr/lib64 \
 CPPFLAGS="-I/usr/include/nss3"

make %{?_smp_mflags}

%install
%make_install

# Make rpm accessible in usrbin
#mv %{buildroot}/bin/rpm %{buildroot}%{_bindir}/rpm
#rmdir %{buildroot}/bin

# Fix up symlinks that point to /bin/rpm
ln -sf rpm %{buildroot}%{_bindir}/rpmquery
ln -sf rpm %{buildroot}%{_bindir}/rpmverify

# this ensures perl doesnt go boom
rm %{buildroot}/usr/lib/rpm/fileattrs/perl.attr
rm %{buildroot}/usr/lib/rpm/fileattrs/perllib.attr

# since post-install hook is disabled on line1, replicate the
# behaviour of stripping libtool .la files
find %{buildroot} -name "*.la" -delete

rm -rf %{buildroot}/usr/bin
rm -rf %{buildroot}/usr/share
rm -rf %{buildroot}/usr/lib/rpm
rm -rf %{buildroot}/usr/lib64
rm -rf %{buildroot}/usr/include




%check
make check


%files 
/usr/lib/python2*
