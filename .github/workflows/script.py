name: Build BCV
'on':
  push:
    branches:
    - master
  pull_request:
    branches:
    - master
jobs:
  build:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        java: '11'
    steps:
    - uses: actions/checkout@v2
    - name: Set up JDK ${{ matrix.java }}
      uses: actions/setup-java@v2
      with:
        java-version: ${{ matrix.java }}
        distribution: temurin
    - name: Build with Maven
      run: mvn -B package --file pom.xml
    - name: Extract Maven project version
      run: echo ::set-output name=version::$(mvn -q -Dexec.executable=echo -Dexec.args='${project.version}'
        --non-recursive exec:exec)
      id: project
    - name: Upload Artifact
      uses: actions/upload-artifact@v2
      if: ${{ matrix.java == '8' }}
      with:
        name: Bytecode-Viewer-${{ steps.project.outputs.version }}-SNAPSHOT
        path: target/Bytecode-Viewer-${{ steps.project.outputs.version }}.jar
        retention-days: 90
