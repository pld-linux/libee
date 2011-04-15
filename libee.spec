#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries
#
Summary:	Event expression library
Name:		libee
Version:	0.3.0
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	http://www.libee.org/files/download/%{name}-%{version}.tar.gz
# Source0-md5:	7d14a7693037d99626299323d9e561a1
URL:		http://www.libee.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libestr-devel
BuildRequires:	libxml2-devel
BuildRequires:	zlib
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Libee is an event expression library that is inspired by the upcoming
CEE standard. Right now, it provides capabilities to generate and emit
messages in a set of standard formats and read a set of different
input formats. Libee also comes with a handy conversion tool that
provides format transformation without the need to program.

%package devel
Summary:	Header files for libee library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libee
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for libee library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libee.

%package static
Summary:	Static libee library
Summary(pl.UTF-8):	Statyczna biblioteka libee
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libee library.

%description static -l pl.UTF-8
Statyczna biblioteka libee.

%prep
%setup -q

%build
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_static_libs:--disable-static}
%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libee.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog
%attr(755,root,root) %{_sbindir}/convert
%attr(755,root,root) %{_libdir}/libee.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libee.so.0

%files devel
%defattr(644,root,root,755)
%{_libdir}/libee.so
%{_includedir}/libee
%{_pkgconfigdir}/libee.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libee.a
%endif
