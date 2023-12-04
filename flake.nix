{
  description = "Nix flake for Transit. A Pythonic Kafka implementation over object storage keyspace";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = {
    flake-utils,
    nixpkgs,
    ...
  }: let
    systems = ["x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin"];
    outputs = flake-utils.lib.eachSystem systems (system: let
      pkgs = import nixpkgs {
        inherit system;
        overlays = [];
      };
    in {
      # packages exported by the flake
      packages = {};

      # nix run
      apps = {};

      # nix fmt
      formatter = pkgs.alejandra;

      # nix develop -c $SHELL
      devShells.default = pkgs.mkShell {
        name = "default dev shell";
        packages = with pkgs;
          [
            ollama
            # python311Packages.nuitka
            python311Packages.python
            python311Packages.pip
            python311Packages.virtualenv
            python311Packages.ipython
            python311Packages.venvShellHook
          ];
        venvDir = ".venv";

        postShellHook = ''
          # k8s
          export KUBECONFIG="$(realpath .)/.local/kubeconfig";
        '';
      };
    });
  in
    outputs;
}
