CREATE TABLE distro (
    id          INT AUTO_INCREMENT,
    name        VARCHAR(50) NOT NULL UNIQUE,
    PRIMARY KEY (id)
);

CREATE TABLE rpm (
    id          INT AUTO_INCREMENT,
    name        VARCHAR(50) NOT NULL UNIQUE,
    PRIMARY KEY(id)
);


INSERT INTO distro VALUES(0, 'openSUSE:10.3');
INSERT INTO distro VALUES(1, 'Java:jpackage-1.7');

