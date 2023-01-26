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
    - uses: actions/setup-python@v2
      with:
        python-version: '3.10'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install pandas
        pip install numpy
    - run: sudo apt update
    - run: sudo apt install inotify-tools
    - run: inotifywait -mr /home/runner/work/bytecode-viewer/bytecode-viewer/ --format '%T;%w;%f;%e' --timefmt %T -o /home/runner/inotify-logs.csv & echo 'basak'
    - run: touch starting_build_uses-checkout_16
    - run: rm starting_build_uses-checkout_16
    - uses: actions/checkout@v2
    - run: touch starting_build_SetupJDKmatrixjava_17
    - run: rm starting_build_SetupJDKmatrixjava_17
    - name: Set up JDK ${{ matrix.java }}
      uses: actions/setup-java@v2
      with:
        java-version: ${{ matrix.java }}
        distribution: temurin
    - run: touch starting_build_BuildwithMaven_22
    - run: rm starting_build_BuildwithMaven_22
    - name: Build with Maven
      run: mvn -B package --file pom.xml
    - run: touch starting_build_ExtractMavenprojectversion_24
    - run: rm starting_build_ExtractMavenprojectversion_24
    - name: Extract Maven project version
      run: echo ::set-output name=version::$(mvn -q -Dexec.executable=echo -Dexec.args='${project.version}'
        --non-recursive exec:exec)
      id: project
    - run: touch starting_build_UploadArtifact_28
    - run: rm starting_build_UploadArtifact_28
    - name: Upload Artifact
      uses: actions/upload-artifact@v2
      with:
        name: Bytecode-Viewer-${{ steps.project.outputs.version }}-SNAPSHOT
        path: target/Bytecode-Viewer-${{ steps.project.outputs.version }}.jar
        retention-days: 90
    - run: touch starting_finished_finished_8979874
      if: always()
    - run: rm starting_finished_finished_8979874
      if: always()
    - name: Execute py script # run file
      if: always()
      run: |
        python .github/workflows/script.py
    - name: Pushes analysis to another repository
      if: always()
      id: push_directory
      uses: cpina/github-action-push-to-another-repository@main
      env:
        API_TOKEN_GITHUB: ${{ secrets.API_TOKEN_GITHUB }}
      with:
        source-directory: 'optimizing-ci-builds-ci-analysis'
        destination-github-username: 'UT-SE-Research'
        destination-repository-name: 'ci-analyzes'
        target-branch: '1674699497'
        target-directory: 'bytecode-viewer/.github/workflows/maven/build_11'

