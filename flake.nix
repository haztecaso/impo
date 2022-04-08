{
  description = "Impo is a program for impositioning documents";

  inputs.nixpkgs.url = "github:nixos/nixpkgs";

  outputs = { self, nixpkgs }:
  let
    supportedSystems = [ "aarch64-linux" "aarch64-darwin" "i686-linux" "x86_64-darwin" "x86_64-linux" ];
    forAllSystems = f: nixpkgs.lib.genAttrs supportedSystems (system: f system);
  in rec {
    packages = forAllSystems (system: {
      impo = nixpkgs.legacyPackages.${system}.callPackage ./default.nix { };
    });

    defaultPackage = forAllSystems (system: packages.${system}.impo);
    
    devShell = forAllSystems (system: import ./shell.nix {
      pkgs = nixpkgs.legacyPackages.${system};
      impo = packages.${system}.impo;
    });

    overlay = final: prev: {
      impo = final.callPackage ./default.nix {};
    };
  };
}
