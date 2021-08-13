{ pkgs, lib }:
with pkgs.python38Packages;
buildPythonPackage rec {
  pname = "impo";
  version = "2.1.1";

  src = ./.;

  propagatedBuildInputs = [ pypdf2 docopt ];

  checkInputs = [ pytest ];
  checkPhase = "pytest";

  meta = with lib; {
    homepage = "https://github.com/haztecaso/impo";
    description = "Impo is a program for impositioning documents";
    license = licenses.gpl3;
  };
}

