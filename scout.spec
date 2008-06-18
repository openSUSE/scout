#
# spec file for package scout
#

# norootforbuild

Name:           scout
Version:        0.0.2
Release:        1
Url:            http://repo.or.cz/w/scout.git
License:        GPL v2 or later
Group:          System/Packages
Summary:        Package Scout
Source:         %{name}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires:  python
Requires:       python

%if 0%{?suse_version}
BuildRequires:  python-xml
%endif

%if 0%{?fedora_version} || 0%{?rhel_version} || 0%{?centos_version}
%define py_sitedir %(python -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")
%endif

%description

Package Scout for indexing various properties of packages, like:
* autoconf macros
* binaries
* Java classes

%prep
%setup -q -n %{name}

%build
python -mcompileall .

%install
# install python scripts
mkdir -p $RPM_BUILD_ROOT%{py_sitedir}/%{name}
cp -a __init__.py{,c} $RPM_BUILD_ROOT%{py_sitedir}/%{name}
shopt -s extglob
cp -a modules/!(foo).py{,c} $RPM_BUILD_ROOT%{py_sitedir}/%{name}
# install data files
install -D -m 0644 repos.conf $RPM_BUILD_ROOT%{_datadir}/%{name}/repos.conf
# create symlinks
install -D -m 0755 scout.py $RPM_BUILD_ROOT%{_bindir}/%{name}
ln -s %{name} $RPM_BUILD_ROOT%{_bindir}/%{name}csv
ln -s %{name} $RPM_BUILD_ROOT%{_bindir}/%{name}xml
# install bash completion
install -D -m 0644 scout.sh $RPM_BUILD_ROOT%{_sysconfdir}/bash_completion.d/scout

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc AUTHORS README
%{_bindir}/%{name}*
%{py_sitedir}/%{name}
%{_datadir}/%{name}
%{_sysconfdir}/bash_completion.d/*

%changelog
