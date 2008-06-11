#
# spec file for package scout
#

# norootforbuild

%define gitrev replace_this_with_the_real_git_revision!
%define pkgver 0.0.1

%py_requires
Name:           scout
Version:        %{pkgver}
Release:        1
Url:            http://repo.or.cz/w/scout.git
License:        GPL v2 or later
Group:          System/Packages
Summary:        Package Scout
Source:         %{name}-%{gitrev}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

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
mkdir -p $RPM_BUILD_ROOT%{datadir}/%{name}
cp -a repos.conf $RPM_BUILD_ROOT%{datadir}/%{name}
# create symlink
ln -s %{py_sitedir}/%{name}/scout.py %{_bindir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc AUTHORS
%{_bindir}/%{name}
%dir %{py_sitedir}/%{name}
%{py_sitedir}/%{name}/*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*

%changelog
