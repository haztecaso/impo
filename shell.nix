{ pkgs ? import <nixpkgs> {} }:
let
  inherit (pkgs) lib;
  impo = import ./default.nix { inherit pkgs lib; };
in
pkgs.mkShell {
  nativeBuildInputs = [ impo ];
}
