#----------------------------------------------------------#
#   Instruction (in Korean) for the Original C Pipeline   #
# Note: I do not recommend to use this C pipeline. Please  #
#       use recently programmed Python version, ASTRiDE.   #
#----------------------------------------------------------#

 첨부한 파일에는 c source와 샘플 fits 파일이 들어있습니다.
make 치면 streak 이라는 실행파일이 생기는데,
실행 방법은,

./streak long.fits 3 100

이라고 하면 100 pixel 보다 길고 sky deviation 보다 3 배 밝은 녀석들만
탐색하라는 명령이 됩니다. (sky 부분 교체가 필요할 것 같은데, 귀국해서
교체한 후에 해당 c source 파일만 다시 보내드릴께요. threshold 부분도 현재
프로그램에서 조금 애매하게 적용되고 있는데.. 이 부분은 좀더 검토후에 알려드릴께요.)

image subtraction이나 기타 방법을 써서 일반 별들을 제거한 후라면, 길이제한을
두지 않더라도 false detection이 별로 나오지 않습니다.
하지만, 일반 영상에 (특히 별이 밀집한 영상의 경우) 적용하면
false 가 많이 나오는데, 그 때 적절한 길이 제한으로 걸러 주시면 됩니다.

streak 탐색 방법에 대해 간단하게 설명하면,
1. threshold 보다 높은 pixel들의 외곽선을 작성.
2. 해당 외곽선이 둥근지 길쭉한 모양인지 판별.
3. 길쭉한 모양이라고 판단될 경우 텍스트 파일로 저장.
4. 저장된 각각의 streak 간의 연관성 판별.
  - 원래는 하나의 streak인데, 영상에서 중간 중간 끊어짐으로써 여러개의 streak
   으로 검출된 경우, 하나로 연결해주는 역할.
  - 각 streak 의 기울기와 서로간의 거리로 판별.

위 과정을 거치면 결과 파일이 두 개가 나오는데, 하나는
fits_file_name.out.txt로 각각의 streak 검출 결과를 저장한 파일이고,
다른 하나는 fits_file_name.dat 로 위 4번의 과정을 거친후
연관성이 있는 streak들을 하나로 합쳐서 저장하는 파일인데, jpeg 파일 만들기 좋게
x, y 위치를 임의로 변경한 거라서 무시하시는게 나을 것 같습니다.

*.out.txt 형태는 다음과 같습니다.

#No xmin ymin xmax ymax   slope   NSTAR dev flat length  correlation
  1   20  323  184  338 -0.085462    0 2.574810  0.984215  163.114655 2
  2  182  309  342  324 -0.090107    0 3.225879  0.979777  159.516296 -1

다른건 설명안드려도 아실테고요 (혹은 무시해도 되는 값들...),
flat과 correlation 이 중요한데, flat 은 1에 가까운 값을 가질수록 streak이 길쭉하다는 것을 나타냅니다.
correlation은 현재 streak과 연결된 녀석이 있을 경우 연결되는 녀석의 No 값입니다.
위의 예에서 보자면 1 번 streak의 correlation 값이 2로 되있으므로
1번 streak이 2번과 연결되어 있다는 것이고요. -1 은 (더 이상) 연결되는 streak 이 없다는 뜻입니다.