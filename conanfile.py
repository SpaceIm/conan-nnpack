from conans import ConanFile, CMake, tools
import glob
import os


class NnpackConan(ConanFile):
    name = "nnpack"
    description = "NNPACK is an acceleration package for neural network computations."
    license = "BSD-2-Clause"
    topics = ("conan", "nnpack", "neural-network", "inference", "multithreading",
              "matrix-multiplication", "simd")
    homepage = "https://github.com/Maratyszcza/NNPACK"
    url = "https://github.com/conan-io/conan-center-index"

    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
    }

    exports_sources = "CMakeLists.txt"
    generators = "cmake"
    _cmake = None

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            del self.options.fPIC
        del self.settings.compiler.libcxx
        del self.settings.compiler.cppstd

    def requirements(self):
        self.requires("cpuinfo/cci.20201217")
        self.requires("fp16/cci.20200514")
        self.requires("fxdiv/cci.20200417")
        self.requires("psimd/cci.20200517")
        self.requires("pthreadpool/cci.20210218")

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        extracted_dir = glob.glob("NNPACK-*")[0]
        os.rename(extracted_dir, self._source_subfolder)

    def _configure_cmake(self):
        if self._cmake:
            return self._cmake
        self._cmake = CMake(self)
        self._cmake.definitions["NNPACK_BACKEND"] = "psimd"
        self._cmake.definitions["NNPACK_CONVOLUTION_ONLY"] = False
        self._cmake.definitions["NNPACK_INFERENCE_ONLY"] = False
        self._cmake.definitions["NNPACK_CUSTOM_THREADPOOL"] = False
        self._cmake.definitions["NNPACK_LIBRARY_TYPE"] = "default"
        self._cmake.definitions["XNNPACK_BUILD_BENCHMARKS"] = False
        self._cmake.definitions["NNPACK_BUILD_TESTS"] = False
        self._cmake.definitions["CPUINFO_SOURCE_DIR"] = ""
        self._cmake.definitions["FP16_SOURCE_DIR"] = ""
        self._cmake.definitions["FXDIV_SOURCE_DIR"] = ""
        self._cmake.definitions["PSIMD_SOURCE_DIR"] = ""
        self._cmake.definitions["PTHREADPOOL_SOURCE_DIR"] = ""
        self._cmake.configure()
        return self._cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy("LICENSE", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["nnpack"]
