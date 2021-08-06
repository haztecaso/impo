{ pkgs ? import <nixpkgs> {} }:
let
  inherit (pkgs) lib;
  impo = import ./default.nix { inherit pkgs lib; };
in
pkgs.mkShell {
  nativeBuildInputs = [ impo pkgs.python38Packages.pypdf2 ];
  shellHook = ''
    alias impo="python -m impo"
  '';
}
