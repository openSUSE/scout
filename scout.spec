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

# workaround conflicting readline packages
%if 0%{?suse_version} <= 1020
BuildRequires:  readline
%endif

%description

Package Scout for indexing various properties of packages, like:
* autoconf macros
* binaries
* Java classes
* Python modules
* webpin web search (http://packages.opensuse-community.org/)

%prep
%setup -q -n %{name}

%build
# compile scripts
python -mcompileall .

%install
# install python scripts
mkdir -p $RPM_BUILD_ROOT%{py_sitedir}/%{name}
shopt -s extglob
cp -a scout/!(foo).py{,c} $RPM_BUILD_ROOT%{py_sitedir}/%{name}
# install data files
install -D -m 0644 repos.conf $RPM_BUILD_ROOT%{_datadir}/%{name}/repos.conf
# create symlinks
install -D -m 0755 scout-cmd.py $RPM_BUILD_ROOT%{_bindir}/%{name}
# install bash completion
install -D -m 0644 scout-bash-completion $RPM_BUILD_ROOT%{_sysconfdir}/bash_completion.d/scout
# install manpage
install -D -m 0644 doc/scout.1 $RPM_BUILD_ROOT%{_mandir}/man1/scout.1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc AUTHORS LICENSE README TODO doc/scout.html doc/scout.pdf
%{_bindir}/%{name}*
%{py_sitedir}/%{name}
%{_datadir}/%{name}
%{_sysconfdir}/bash_completion.d/*
%{_mandir}/man1/*

%changelog
