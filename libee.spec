#
# Conditional build:
%bcond_without	static_libs	# static library
#
Summary:	Event expression library
Summary(pl.UTF-8):	Biblioteka wyrażeń dotyczących zdarzeń
Name:		libee
Version:	0.4.1
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	http://www.libee.org/files/download/%{name}-%{version}.tar.gz
# Source0-md5:	7bbf4160876c12db6193c06e2badedb2
URL:		http://www.libee.org/
BuildRequires:	autoconf >= 2.61
BuildRequires:	automake
BuildRequires:	libestr-devel
BuildRequires:	libtool
BuildRequires:	libxml2-devel
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Libee is an event expression library that is inspired by the upcoming
CEE standard. Right now, it provides capabilities to generate and emit
messages in a set of standard formats and read a set of different
input formats. Libee also comes with a handy conversion tool that
provides format transformation without the need to program.

%description -l pl.UTF-8
Libee to biblioteka wyrażeń dotychących zdarzeń, zainspirowana
nadchodzącym standardem CEE. Obecnie daje możliwość generowania i
wysyłania komunikatów w zbiorze standardowych formatów oraz czytania
zbioru innych formatów wejściowych. Pakiet zawiera także podręczne
narzędzie do konwersji, pozwalające na przekształcanie formatów bez
potrzeby pisania programu.

%package devel
Summary:	Header files for libee library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libee
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libestr-devel

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
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static}

# make can't resolve $(top_builddir)/src/libee.la dependency
%{__make} -C src libee.la

%{__make}

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
%attr(755,root,root) %{_sbindir}/libee-convert
%attr(755,root,root) %{_libdir}/libee.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libee.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libee.so
%{_includedir}/libee
%{_pkgconfigdir}/libee.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libee.a
%endif
