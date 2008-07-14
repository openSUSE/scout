#
# spec file for command-not-found
#

BuildRequires:  python rpm-python
Name:           command-not-found
Version:        0.1.0
Release:        1
Url:            http://en.opensuse.org/Scout
License:        MIT License
Group:          System/Shells
Summary:        Command Not Found extension for shell
Source:         %{name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Requires:       python rpm-python
Requires:       bash(CommandNotFound)
%if 0%{?suse_version} > 1030
%define distro suse110
%endif
%if 0%{?suse_version} <= 1030 && 0%{?suse_version} > 1020
%define distro suse103
%endif
%if 0%{?suse_version} <= 1020 && 0%{?suse_version} > 1010
%define distro suse102
%endif
%if 0%{?suse_version} <= 1010 && 0%{?suse_version} > 1000
%define distro suse101
%endif
Requires:       scout-bin-%{distro}

%description

The "command not found" message is not very helpful. If e.g. the unzip command
is not found but it's available in a package, it would be very interesting
if the system could tell that the command is currently not available,
but installing a package would provide it.

%prep
%setup -q

%build

%install
install -D -m 755 command-not-found $RPM_BUILD_ROOT%{_bindir}/command-not-found
for shell in bash zsh; do
    install -D -m 644 command_not_found_${shell} $RPM_BUILD_ROOT%{_sysconfdir}/${shell}_command_not_found
    sed -i 's:__DISTRO__:%{distro}:' $RPM_BUILD_ROOT%{_sysconfdir}/${shell}_command_not_found
done

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS COPYING README TODO
%{_sysconfdir}/*
%{_bindir}/*

%changelog
