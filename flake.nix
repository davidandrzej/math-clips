{
  # Context: getting some of the graphics backends for manim (ce)
  # to work on apple silicon was kind of a mess... 
  description = "Python project with overlay for moderngl";

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
            moderngl = pySelf.buildPythonPackage rec {
              pname = "moderngl";
              version = "5.12.0";
              pyproject = true;
              src = pySelf.fetchPypi {
                inherit pname version;
                hash = "sha256-UpNqmMyy8uHW48sYUospGfaDHn4/kk54i1hzutzlEps=";
              };
              nativeBuildInputs = [ pySelf.setuptools-scm ];

              propagatedBuildInputs = [ pySelf.glcontext ];
            };

            # On Apple Silicon, nixpkgs' moderngl-window dependency chain currently
            # evaluates linux-only OpenGL stack inputs (glibc), which prevents the
            # shell from even loading. The Cairo renderer path does not need
            # moderngl-window, so we drop it on Darwin to keep a working dev shell.
            manim = if prev.stdenv.isDarwin then
              pySuper.manim.overridePythonAttrs (old: {
                dependencies = prev.lib.filter
                  (pkg: (prev.lib.getName pkg) != "moderngl-window")
                  (old.dependencies or [ ]);

                propagatedBuildInputs = prev.lib.filter
                  (pkg: (prev.lib.getName pkg) != "moderngl-window")
                  (old.propagatedBuildInputs or [ ]);
              })
            else
              pySuper.manim;
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
            p.manim
            p.glcontext
            p.moderngl
          ]))
          pkgs.ffmpeg
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
