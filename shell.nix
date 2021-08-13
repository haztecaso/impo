{ pkgs ? import <nixpkgs> {} }:
let
  inherit (pkgs) lib;
  impo = import ./default.nix { inherit pkgs lib; };
in
pkgs.mkShell {
  nativeBuildInputs = with pkgs.python38Packages; [
    impo
    pypdf2
    docopt
    pytest
  ];
  shellHook = ''
    alias impo="python -m impo"
    alias pytest="python -m pytest"
  '';
}
