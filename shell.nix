{ pkgs, impo }:
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
