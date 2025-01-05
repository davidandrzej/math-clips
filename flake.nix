{
  description = "Python project with an overlay for moderngl";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
    let
      myOverlay = final: prev: {
        python3_12 = prev.python312.override {
          packageOverrides = pySelf: pySuper: {
            glcontext = pySelf.buildPythonPackage rec {
              pname = "glcontext";
              version = "3.0.0";
              pyproject = true;
              src = pySelf.fetchPypi {
                inherit pname version;
                hash = "sha256-VxaO3NON8vwNcMMY7fb35ZCR+6HNPa2yidCqUESSEe8=";
              };
              nativeBuildInputs = [ pySelf.setuptools-scm ];
            };
            moderngl = builtins.trace "Overriding moderngl from myOverlay" (
              pySelf.buildPythonPackage rec {
                pname = "moderngl";
                version = "5.12.0";
                pyproject = true;
                src = pySelf.fetchPypi {
                  inherit pname version;
                  hash = "sha256-UpNqmMyy8uHW48sYUospGfaDHn4/kk54i1hzutzlEps=";
                };
                nativeBuildInputs = [ pySelf.setuptools-scm ];

                # This line is critical:
                propagatedBuildInputs = [ pySelf.glcontext ];
              }
            );
          };
        };
        python3 = final.python3_12;
      };

      pkgs = import nixpkgs {
        inherit system;
        overlays = [ myOverlay ];
      };
    in {
      devShells.default = pkgs.mkShell {
        name = "my-devshell";

        packages = [
          (pkgs.python3.withPackages (p: [            
            p.glcontext
            p.moderngl
          ]))
        ];

        shellHook = ''
          echo "Using Python: $(python --version)"
          echo "moderngl version: $(python -c "import moderngl; print(moderngl.__version__)")"
          echo "glcontext version: $(python -c "import glcontext; print(glcontext.__version__)")"
        '';
      };
    }
  );
}
