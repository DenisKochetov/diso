import glob
import os
from setuptools import find_packages, setup
from torch.utils.cpp_extension import BuildExtension


class DeferredBuildExtension(BuildExtension):
    def build_extensions(self):
        import torch
        from torch.utils.cpp_extension import CUDA_HOME, CUDAExtension, CppExtension

        main_file = [os.path.join("src", "pybind.cpp")]
        source_cuda = glob.glob(os.path.join("src", "*.cu"))
        sources = list(main_file)
        extension = CppExtension
        define_macros = []
        extra_compile_args = {}

        if (torch.cuda.is_available() and CUDA_HOME is not None) or os.getenv("FORCE_CUDA", "0") == "1":
            extension = CUDAExtension
            sources += source_cuda
            define_macros += [("WITH_CUDA", None)]
            nvcc_flags = os.getenv("NVCC_FLAGS", "")
            nvcc_flags = nvcc_flags.split(" ") if nvcc_flags else ["-O3"]
            extra_compile_args = {
                "cxx": ["-O3"],
                "nvcc": nvcc_flags,
            }

        self.extensions = [
            extension(
                "diso._C",
                sources,
                include_dirs=["src"],
                define_macros=define_macros,
                extra_compile_args=extra_compile_args,
            )
        ]
        super().build_extensions()


setup(
    name="diso",
    version="0.1.4",
    author="Xiwei",
    author_email="xiwei@ucsd.edu",
    description="Differentiable Iso-Surface Extraction Package",
    keywords="differentiable iso-surface extraction",
    license="CC BY-NC 4.0",
    classifiers=[
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Other Audience",
        "Intended Audience :: Science/Research",
        "Natural Language :: English",
        "Framework :: Robot Framework :: Tool",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
    python_requires=">=3.6",
    install_requires=["trimesh"],
    packages=find_packages(exclude=["tests"]),
    ext_modules=[],  # extensions are added later inside build_ext
    cmdclass={"build_ext": DeferredBuildExtension.with_options(no_python_abi_suffix=True)},
    zip_safe=False,
)
