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
BuildRequires:  python python-xml
Requires:       python

%description

Scout for indexing various properties of packages:
* autoconf macros
* binaries
* Java classes

%prep
%setup -q -n %{name}

%build
python -mcompileall .
python -O -mcompileall .

%install
# install python scripts
mkdir -p $RPM_BUILD_ROOT%{py_sitedir}/%{name}/modules
cp -a __init__.py{,c,o} $RPM_BUILD_ROOT%{py_sitedir}/%{name}
cp -a modules/*.py{,c,o} $RPM_BUILD_ROOT%{py_sitedir}/%{name}/modules
# install data files
install -D -m 0644 repos.conf $RPM_BUILD_ROOT%{_datadir}/%{name}/repos.conf
# create symlinks
install -D -m 0755 scout.py $RPM_BUILD_ROOT%{_bindir}/%{name}
ln -s %{name} $RPM_BUILD_ROOT%{_bindir}/%{name}csv
ln -s %{name} $RPM_BUILD_ROOT%{_bindir}/%{name}xml

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc AUTHORS
%{_bindir}/%{name}*
%{py_sitedir}/%{name}
%{_datadir}/%{name}

%changelog
