#
# spec file for package scout
#

# norootforbuild

Name:           scout
Version:        0.0.1
Release:        1
Url:            http://repo.or.cz/w/scout.git
License:        GPL v2 or later
Group:          System/Packages
Summary:        Package Scout
Source:         %{name}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires:  python
Requires:       python

%description

Scout for indexing various properties of packages:
* autoconf macros
* binaries
* Java classes

%prep
%setup -q -n %{name}

%build

%install
# install python scripts
mkdir -p $RPM_BUILD_ROOT%{py_sitedir}/%{name}/modules
cp -a *.py $RPM_BUILD_ROOT%{py_sitedir}/%{name}
cp -a modules/*.py $RPM_BUILD_ROOT%{py_sitedir}/%{name}/modules
# install data files
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -a repos.conf $RPM_BUILD_ROOT%{_datadir}/%{name}
# create symlinks
mkdir -p $RPM_BUILD_ROOT%{_bindir}
ln -s %{py_sitedir}/%{name}/scout.py $RPM_BUILD_ROOT%{_bindir}/%{name}
ln -s %{name} $RPM_BUILD_ROOT%{_bindir}/%{name}csv
ln -s %{name} $RPM_BUILD_ROOT%{_bindir}/%{name}xml

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc AUTHORS
%{_bindir}/%{name}*
%dir %{py_sitedir}/%{name}
%{py_sitedir}/%{name}/*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*

%changelog
