{ pkgs, lib }:
with pkgs.python38Packages;
buildPythonPackage rec {
  pname = "imposicion";
  version = "0.0.1";

  src = ./.;

  propagatedBuildInputs = [ pypdf2 ];

  meta = with lib; {
    homepage = "https://git.haztecaso.com/impo";
    description = "Impo is a program for impositioning documents";
    license = licenses.gpl3;
  };
}

