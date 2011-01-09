Summary:	Chasm - tool to improve C++ and Fortran 90 interoperability
Summary(pl.UTF-8):	Chasm - narzędzie do poprawy współpracy C++ z Fortranem 90
Name:		chasm
Version:	1.4
%define	subver	RC3
Release:	0.%{subver}.1
License:	MIT-like
Group:		Libraries
# note: old chasm_1.4 tarball is older than 1.4RC3
Source0:	http://downloads.sourceforge.net/chasm-interop/%{name}_%{version}.%{subver}.tar.gz
# Source0-md5:	e7db64f14c47a6122b02d66fe1e2bd8b
URL:		http://chasm-interop.sourceforge.net/
BuildRequires:	gcc-fortran >= 5:4.0
BuildRequires:	libstdc++-devel
BuildRequires:	pdtoolkit-devel >= 3.0
BuildRequires:	xalan-j
Suggests:	pdtoolkit >= 3.0
Suggests:	xalan-j
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Chasm is a tool to improve C++ and Fortran 90 interoperability. Chasm
parses Fortran 90 source code and automatically generates C++ bridging
code that can be used in C++ programs to make calls to Fortran
routines. It also automatically generates C structs that provide a
bridge to Fortran derived types. Chasm supplies a C++ array descriptor
class which provides an interface between C and F90 arrays. This
allows arrays to be created in one language and then passed to and
used by the other language.

%description -l pl.UTF-8
Chasm to narzędzie poprawiające współpracę między C++ a Fortranem 90.
Analizuje kod źródłowy w Fortranie 90 i automatycznie generuje kod
pomostowy C++, który można używać w programach w C++ w celu
wywoływania procedur w Fortranie. Ponadto automatycznie generuje
struktury C będące pomostem do typów wywodzących się z Fortrana.
Dostarcza klasę C++ opisu tablicy, udostępniającą interfejs między
tablicami C i F90. Pozwala to na tworzenie tablic w jednym języku i
przekazywanie ich do drugiego.

%prep
%setup -q -n %{name}

%build
%configure \
	--enable-pdt \
	--with-F90-vendor=GNU \
	--with-pdt-root=%{_libdir}/pdtoolkit \
	--with-xalan-root=/usr/share/java

# pass CXX/CCFLAGS for xmlgen
%{__make} \
	CXX="%{__cxx}" \
	CCFLAGS="%{rpmcxxflags} -Wall -I\$(INC)"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	CHASM_BIN=$RPM_BUILD_ROOT%{_bindir} \
	CHASM_INCLUDE=$RPM_BUILD_ROOT%{_includedir} \
	CHASM_LIBS=$RPM_BUILD_ROOT%{_libdir} \
	datadir=$RPM_BUILD_ROOT%{_datadir} \
	mandir=$RPM_BUILD_ROOT%{_mandir}/man1

mv -f $RPM_BUILD_ROOT%{_datadir}/mapping.dtd $RPM_BUILD_ROOT%{_datadir}/xform/mapping.dtd

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE README
%attr(755,root,root) %{_bindir}/chasm-config
%attr(755,root,root) %{_bindir}/xmlgen
%{_libdir}/libchasm.a
%{_libdir}/f90_*.mod
%{_includedir}/CompilerCharacteristics.h
%{_includedir}/F90*.h
%{_includedir}/MakeIncl.chasm
%{_includedir}/compilers
%{_datadir}/xform
