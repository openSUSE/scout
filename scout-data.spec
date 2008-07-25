#
# spec file for package scout data
#

# norootforbuild

Name:           scout-data
Version:        0
Release:        1
Url:            http://en.opensuse.org/Scout
License:        MIT License
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires:  python lzma sqlite
Requires:       scout
Group:          System/Packages
Summary:        Index Data for Package Scout
BuildArch:      noarch

Source:         scout-gen.tar.bz2

Source10:       autoconf-sle10.txt.lzma
Source11:       autoconf-suse101.txt.lzma
Source12:       autoconf-suse102.txt.lzma
Source13:       autoconf-suse103.txt.lzma
Source14:       autoconf-suse110.txt.lzma

Source20:       bin-packman103.txt.lzma
Source21:       bin-packman110.txt.lzma
Source22:       bin-sle10.txt.lzma
Source23:       bin-suse101.txt.lzma
Source24:       bin-suse102.txt.lzma
Source25:       bin-suse103.txt.lzma
Source26:       bin-suse110.txt.lzma

Source30:       java-jpackage17.txt.lzma
Source31:       java-sle10.txt.lzma
Source32:       java-suse101.txt.lzma
Source33:       java-suse102.txt.lzma
Source34:       java-suse103.txt.lzma
Source35:       java-suse110.txt.lzma

Source40:       python-sle10.txt.lzma
Source41:       python-suse101.txt.lzma
Source42:       python-suse102.txt.lzma
Source43:       python-suse103.txt.lzma
Source44:       python-suse110.txt.lzma

Source50:       header-sle10.txt.lzma
Source51:       header-suse101.txt.lzma
Source52:       header-suse102.txt.lzma
Source53:       header-suse103.txt.lzma
Source54:       header-suse110.txt.lzma

%description
Index Data for Package Scout

%package -n scout-autoconf-sle10
Group:          System/Packages
Summary:        Index Data for Package Scout
Version:        2008.06.17
Requires:       scout

%description -n scout-autoconf-sle10
Package Scout Index Data - Autoconf macros from SUSE Linux Enterprise 10

%package -n scout-autoconf-suse101
Group:          System/Packages
Summary:        Index Data for Package Scout
Version:        2008.06.16
Requires:       scout

%description -n scout-autoconf-suse101
Package Scout Index Data - Autoconf macros from SUSE Linux 10.1

%package -n scout-autoconf-suse102
Group:          System/Packages
Summary:        Index Data for Package Scout
Version:        2008.06.16
Requires:       scout

%description -n scout-autoconf-suse102
Package Scout Index Data - Autoconf macros from openSUSE 10.2

%package -n scout-autoconf-suse103
Group:          System/Packages
Summary:        Index Data for Package Scout
Version:        2008.06.16
Requires:       scout

%description -n scout-autoconf-suse103
Package Scout Index Data - Autoconf macros from openSUSE 10.3

%package -n scout-autoconf-suse110
Group:          System/Packages
Summary:        Index Data for Package Scout
Version:        2008.06.16
Requires:       scout

%description -n scout-autoconf-suse110
Package Scout Index Data - Autoconf macros from openSUSE 11.0

%package -n scout-bin-packman103
Group:          System/Packages
Summary:        Index Data for Package Scout
Version:        2008.06.20
Requires:       scout

%description -n scout-bin-packman103
Package Scout Index Data - Binaries from Packman for openSUSE 10.3

%package -n scout-bin-packman110
Group:          System/Packages
Summary:        Index Data for Package Scout
Version:        2008.06.20
Requires:       scout

%description -n scout-bin-packman110
Package Scout Index Data - Binaries from Packman for openSUSE 11.0

%package -n scout-bin-sle10
Group:          System/Packages
Summary:        Index Data for Package Scout
Version:        2008.06.17
Requires:       scout

%description -n scout-bin-sle10
Package Scout Index Data - Binaries from SUSE Linux Enterprise 10

%package -n scout-bin-suse101
Group:          System/Packages
Summary:        Index Data for Package Scout
Version:        2008.06.14
Requires:       scout

%description -n scout-bin-suse101
Package Scout Index Data - Binaries from SUSE Linux 10.1

%package -n scout-bin-suse102
Group:          System/Packages
Summary:        Index Data for Package Scout
Version:        2008.06.14
Requires:       scout

%description -n scout-bin-suse102
Package Scout Index Data - Binaries from openSUSE 10.2

%package -n scout-bin-suse103
Group:          System/Packages
Summary:        Index Data for Package Scout
Version:        2008.06.14
Requires:       scout

%description -n scout-bin-suse103
Package Scout Index Data - Binaries from openSUSE 10.3

%package -n scout-bin-suse110
Group:          System/Packages
Summary:        Index Data for Package Scout
Version:        2008.06.14
Requires:       scout

%description -n scout-bin-suse110
Package Scout Index Data - Binaries from openSUSE 11.0

%package -n scout-java-jpackage17
Group:          System/Packages
Summary:        Index Data for Package Scout
Version:        2008.06.14
Requires:       scout

%description -n scout-java-jpackage17
Package Scout Index Data - Java classes from Jpackage 1.7

%package -n scout-java-sle10
Group:          System/Packages
Summary:        Index Data for Package Scout
Version:        2008.06.14
Requires:       scout

%description -n scout-java-sle10
Package Scout Index Data - Java classes from SUSE Linux Enterprise 10

%package -n scout-java-suse101
Group:          System/Packages
Summary:        Index Data for Package Scout
Version:        2008.06.14
Requires:       scout

%description -n scout-java-suse101
Package Scout Index Data - Java classes from SUSE Linux 10.1

%package -n scout-java-suse102
Group:          System/Packages
Summary:        Index Data for Package Scout
Version:        2008.06.14
Requires:       scout

%description -n scout-java-suse102
Package Scout Index Data - Java classes from openSUSE 10.2

%package -n scout-java-suse103
Group:          System/Packages
Summary:        Index Data for Package Scout
Version:        2008.06.14
Requires:       scout

%description -n scout-java-suse103
Package Scout Index Data - Java classes from openSUSE 10.3

%package -n scout-java-suse110
Group:          System/Packages
Summary:        Index Data for Package Scout
Version:        2008.06.14
Requires:       scout

%description -n scout-java-suse110
Package Scout Index Data - Java classes from openSUSE 11.0

%package -n scout-python-sle10
Group:          System/Packages
Summary:        Index Data for Package Scout
Version:        2008.06.22
Requires:       scout

%description -n scout-python-sle10
Package Scout Index Data - Python modules from SUSE Linux Enterprise 10

%package -n scout-python-suse101
Group:          System/Packages
Summary:        Index Data for Package Scout
Version:        2008.06.22
Requires:       scout

%description -n scout-python-suse101
Package Scout Index Data - Python modules from SUSE Linux 10.1

%package -n scout-python-suse102
Group:          System/Packages
Summary:        Index Data for Package Scout
Version:        2008.06.22
Requires:       scout

%description -n scout-python-suse102
Package Scout Index Data - Python modules from openSUSE 10.2

%package -n scout-python-suse103
Group:          System/Packages
Summary:        Index Data for Package Scout
Version:        2008.06.22
Requires:       scout

%description -n scout-python-suse103
Package Scout Index Data - Python modules from openSUSE 10.3

%package -n scout-python-suse110
Group:          System/Packages
Summary:        Index Data for Package Scout
Version:        2008.06.22
Requires:       scout

%description -n scout-python-suse110
Package Scout Index Data - Python modules from openSUSE 11.0

%package -n scout-header-sle10
Group:          System/Packages
Summary:        Index Data for Package Scout
Version:        2008.07.08
Requires:       scout

%description -n scout-header-sle10
Package Scout Index Data - Headers from SUSE Linux Enterprise 10

%package -n scout-header-suse101
Group:          System/Packages
Summary:        Index Data for Package Scout
Version:        2008.07.08
Requires:       scout

%description -n scout-header-suse101
Package Scout Index Data - Headers from SUSE Linux 10.1

%package -n scout-header-suse102
Group:          System/Packages
Summary:        Index Data for Package Scout
Version:        2008.07.08
Requires:       scout

%description -n scout-header-suse102
Package Scout Index Data - Headers from openSUSE 10.2

%package -n scout-header-suse103
Group:          System/Packages
Summary:        Index Data for Package Scout
Version:        2008.07.08
Requires:       scout

%description -n scout-header-suse103
Package Scout Index Data - Headers from openSUSE 10.3

%package -n scout-header-suse110
Group:          System/Packages
Summary:        Index Data for Package Scout
Version:        2008.07.08
Requires:       scout

%description -n scout-header-suse110
Package Scout Index Data - Headers from openSUSE 11.0

%prep
%setup -q -c -n data-gen
cp -a %{SOURCE10} %{SOURCE11} %{SOURCE12} %{SOURCE13} %{SOURCE14} .
cp -a %{SOURCE20} %{SOURCE21} %{SOURCE22} %{SOURCE23} %{SOURCE24} %{SOURCE25} %{SOURCE26} .
cp -a %{SOURCE30} %{SOURCE31} %{SOURCE32} %{SOURCE33} %{SOURCE34} %{SOURCE35} .
cp -a %{SOURCE40} %{SOURCE41} %{SOURCE42} %{SOURCE43} %{SOURCE44} .
cp -a %{SOURCE50} %{SOURCE51} %{SOURCE52} %{SOURCE53} %{SOURCE54} .

%build
python gen-autoconf.py
python gen-bin.py
python gen-java.py
python gen-python.py
python gen-header.py
sh gen

%install
mkdir -p $RPM_BUILD_ROOT%{_datadir}/scout
cp -a *.db $RPM_BUILD_ROOT%{_datadir}/scout

%clean
rm -rf $RPM_BUILD_ROOT

%files -n scout-autoconf-sle10
%defattr(-,root,root)
%{_datadir}/scout/autoconf-sle10*

%files -n scout-autoconf-suse101
%defattr(-,root,root)
%{_datadir}/scout/autoconf-suse101*

%files -n scout-autoconf-suse102
%defattr(-,root,root)
%{_datadir}/scout/autoconf-suse102*

%files -n scout-autoconf-suse103
%defattr(-,root,root)
%{_datadir}/scout/autoconf-suse103*

%files -n scout-autoconf-suse110
%defattr(-,root,root)
%{_datadir}/scout/autoconf-suse110*

%files -n scout-bin-packman103
%defattr(-,root,root)
%{_datadir}/scout/bin-packman103*

%files -n scout-bin-packman110
%defattr(-,root,root)
%{_datadir}/scout/bin-packman110*

%files -n scout-bin-sle10
%defattr(-,root,root)
%{_datadir}/scout/bin-sle10*

%files -n scout-bin-suse101
%defattr(-,root,root)
%{_datadir}/scout/bin-suse101*

%files -n scout-bin-suse102
%defattr(-,root,root)
%{_datadir}/scout/bin-suse102*

%files -n scout-bin-suse103
%defattr(-,root,root)
%{_datadir}/scout/bin-suse103*

%files -n scout-bin-suse110
%defattr(-,root,root)
%{_datadir}/scout/bin-suse110*

%files -n scout-java-jpackage17
%defattr(-,root,root)
%{_datadir}/scout/java-jpackage17*

%files -n scout-java-sle10
%defattr(-,root,root)
%{_datadir}/scout/java-sle10*

%files -n scout-java-suse101
%defattr(-,root,root)
%{_datadir}/scout/java-suse101*

%files -n scout-java-suse102
%defattr(-,root,root)
%{_datadir}/scout/java-suse102*

%files -n scout-java-suse103
%defattr(-,root,root)
%{_datadir}/scout/java-suse103*

%files -n scout-java-suse110
%defattr(-,root,root)
%{_datadir}/scout/java-suse110*

%files -n scout-python-sle10
%defattr(-,root,root)
%{_datadir}/scout/python-sle10*

%files -n scout-python-suse101
%defattr(-,root,root)
%{_datadir}/scout/python-suse101*

%files -n scout-python-suse102
%defattr(-,root,root)
%{_datadir}/scout/python-suse102*

%files -n scout-python-suse103
%defattr(-,root,root)
%{_datadir}/scout/python-suse103*

%files -n scout-python-suse110
%defattr(-,root,root)
%{_datadir}/scout/python-suse110*

%files -n scout-header-sle10
%defattr(-,root,root)
%{_datadir}/scout/header-sle10*

%files -n scout-header-suse101
%defattr(-,root,root)
%{_datadir}/scout/header-suse101*

%files -n scout-header-suse102
%defattr(-,root,root)
%{_datadir}/scout/header-suse102*

%files -n scout-header-suse103
%defattr(-,root,root)
%{_datadir}/scout/header-suse103*

%files -n scout-header-suse110
%defattr(-,root,root)
%{_datadir}/scout/header-suse110*

%changelog
