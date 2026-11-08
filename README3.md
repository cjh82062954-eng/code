1.프로제그 개요
프로젝트 이름: Python Interactive Quiz Game (mission2)
개발 환경: Python 3.14, VSCode, WSL (Ubuntu)

2. 퀴즈 주제와 선정 이유
 주제: 프로그래밍 및 IT 일반 상식 퀴즈 (Python, Git, 웹, 데이터베이스 등)
 선정 이유 : 개발 학습 과정에서 익혀야 할 핵심 지식을 복습할 수 있도록 구성했습니다. 또한 사용자가 직접 문제를 추가, 조회하고 점수를 누적 관리할 수 있도록  하여 실용성을 높였습니다.

3. 실행 방법 (`Execution`)
 터미널에서 프로젝트 루트 디렉토리로 이동한 뒤 아래 명령어를 입력합니다.
 root@DESKTOP-V60E01R:/mnt/c/Users/USER/Desktop/mission2# python3 main.py

4.기능 목록
 1.퀴즈 풀기: 등록된 퀴즈를 풀고 실시간으로 정답 여부 및 점수를 집계
 2.퀴즈 추가: 사용자가 직접 새로운 문제와 4지선다 선택지, 정답을 입력하여 추가
 3.퀴즈 목록: 현재 등록된 모든 퀴즈 목록을 확인
 4.점수 확인: 역대 최고 기록 확인
 5.데이터 영구 저장: 프로그램 종료 후 재시작해도 퀴즈 목록과 최고 점수가 state.json을 통해 유지됨

5.파일 구조
-main.py
 from game import QuizGame

 if __name__ == "__main__":
     try:
         game = QuizGame()
         game.run()
     except (KeyboardInterrupt, EOFError):
         print("\n\n⚠️ 비정상적인 입력이 감지되었습니다. 안전하게 프로그램을 종료합니다.")

-quize.py
 class Quiz:
     def __init__(self, question, choices, answer):
         self.question = question  # 문제 내용
         self.choices = choices    # 선택지 4개
         self.answer = answer      # 정답 번호 (1~4)

     def display(self):
         """문제와 선택지 출력"""
         print(f"\n[문제] {self.question}")
         for i, choice in enumerate(self.choices, 1):
             print(f"  {i}. {choice}")

     def check_answer(self, user_answer):
         """정답 확인"""
         return self.answer == user_answer
 
     def to_dict(self):
         """JSON 저장을 위해 딕셔너리로 변환"""
         return {
             "question": self.question,
             "choices": self.choices,
             "answer": self.answer
         }

-gmam.py
 import json
 import os
 from quiz import Quiz

 class QuizGame:
     def __init__(self, filename="state.json"):
         self.filename = filename
         self.quizzes = []
         self.best_score = 0
         self.load_data()

     def load_data(self):
         """파일에서 데이터 불러오기 (없거나 손상되면 기본 퀴즈 5개 사용)"""
         default_quizzes = [
             Quiz("Python에서 함수를 정의할 때 사용하는 키워드는?", ["func", "define", "def", "lambda"], 3),
             Quiz("다음 중 수정이 불가능한(immutable) 파이썬 자료형은?", ["list", "dict", "tuple", "set"], 3),
             Quiz("Git에서 현재 작업 중인 파일의 변경 상태를 확인하는 명령어는?", ["git status", "git commit", "git push", "git init"], 1),
             Quiz("파이썬 코드를 실행할 때 터미널에 입력하는 기본 명령어 형식은?", ["run script.py", "python3 script.py", "start script.py",   "exec script.py"], 2),
             Quiz("Git 원격 저장소의 최신 코드를 로컬로 가져와 병합하는 명령어는?", ["git clone", "git push", "git pull", "git fetch"], 3)
         ]

         if not os.path.exists(self.filename):
             self.quizzes = default_quizzes
             self.best_score = 0
             print("📂 저장된 데이터가 없어 기본 퀴즈로 시작합니다.")
             return

         try:
             with open(self.filename, "r", encoding="utf-8") as f:
                 data = json.load(f)
                 loaded_quizzes = [Quiz(q["question"], q["choices"], q["answer"]) for q in data.get("quizzes", [])]
                 self.quizzes = loaded_quizzes if loaded_quizzes else default_quizzes
                self.best_score = data.get("best_score", 0)
                 print(f"📂 저장된 데이터를 불러왔습니다. (퀴즈 {len(self.quizzes)}개, 최고점수 {self.best_score}점)")
         except:
             print("⚠️ 데이터 파일 오류 발생. 기본 데이터로 복구합니다.")
             self.quizzes = default_quizzes
             self.best_score = 0
             self.save_data()

     def save_data(self):
         """state.json 파일에 데이터 저장"""
         data = {
             "quizzes": [q.to_dict() for q in self.quizzes],
             "best_score": self.best_score
         }
         with open(self.filename, "w", encoding="utf-8") as f:
             json.dump(data, f, ensure_ascii=False, indent=4)

     def run(self):
         """게임 메인 메뉴 화면"""
         while True:
             print("\n" + "="*40)
             print("        🎯 나만의 퀴즈 게임 🎯")
             print("="*40)
             print("1. 퀴즈 풀기")
             print("2. 퀴즈 추가")
             print("3. 퀴즈 목록")
             print("4. 점수 확인")
             print("5. 종료")
             print("="*40)

             choice = input("선택: ").strip()

             if choice == "1":
                 self.play_quiz()
             elif choice == "2":
                 self.add_quiz()
             elif choice == "3":
                 self.show_quiz_list()
             elif choice == "4":
                 self.show_score()
             elif choice == "5":
                 print("\n👋 프로그램을 종료합니다!")
                 break
             else:
                 print("⚠️ 잘못된 입력입니다. 1-5 사이의 숫자를 입력하세요.")

     def play_quiz(self):
         """퀴즈 풀기 기능"""
         if not self.quizzes:
             print("⚠️ 등록된 퀴즈가 없습니다.")
             return

         print(f"\n📝 퀴즈를 시작합니다! (총 {len(self.quizzes)}문제)")
         score = 0

         for idx, quiz in enumerate(self.quizzes, 1):
             print("-" * 40)
             print(f"[문제 {idx}]")
             quiz.display()

             while True:
                 ans_input = input("정답 입력 (1-4): ").strip()
                  try:
                     user_ans = int(ans_input)
                     if 1 <= user_ans <= 4:
                         break
                     print("⚠️ 1~4 사이의 숫자를 입력하세요.")
                 except ValueError:
                     print("⚠️ 숫자 형태의 값만 입력할 수 있습니다.")

             if quiz.check_answer(user_ans):
                 print("✅ 정답입니다!")
                 score += 1
             else:
                 print(f"❌ 틀렸습니다! 정답은 {quiz.answer}번입니다.")

         print("\n" + "="*40)
         print(f"🏆 결과: 총 {len(self.quizzes)}문제 중 {score}문제 정답! ({score * 100 // len(self.quizzes)}점)")
         if score > self.best_score:
             self.best_score = score
             print("🎉 새로운 최고 점수입니다!")
             self.save_data()
         print("="*40)

     def add_quiz(self):
         """새로운 퀴즈 추가 기능"""
         print("\n📌 새로운 퀴즈를 추가합니다.")
         question = input("문제를 입력하세요: ").strip()
         if not question:
             print("⚠️ 빈 문장은 입력할 수 없습니다.")
             return

         choices = []
         for i in range(1, 5):
             choice = input(f"선택지 {i}: ").strip()
             if not choice:
                 print("⚠️ 빈 선택지는 허용되지 않습니다.")
                 return
             choices.append(choice)

         while True:
             try:
                 ans_input = input("정답 번호 (1-4): ").strip()
                 answer = int(ans_input)
                 if 1 <= answer <= 4:
                     break
                 print("⚠️ 1~4 사이의 숫자를 입력하세요.")
             except ValueError:
                 print("⚠️ 올바른 숫자를 입력하세요.")

         self.quizzes.append(Quiz(question, choices, answer))
         self.save_data()
         print("✅ 퀴즈가 추가되었습니다!")

     def show_quiz_list(self):
         """등록된 퀴즈 목록 보기"""
         if not self.quizzes:
             print("⚠️ 등록된 퀴즈가 없습니다.")
             return
         print(f"\n📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
         print("-" * 40)
         for idx, q in enumerate(self.quizzes, 1):
             print(f"[{idx}] {q.question}")
         print("-" * 40)

     def show_score(self):
         """최고 점수 확인"""
         print("\n" + "="*40)
         print(f"🏆 최고 점수: {self.best_score}점")
         print("="*40)

6. 데이터 파일 설명 (state.json)
경로: ./state.json (프로젝트 루트 디렉토리)
역할: 프로그램 실행 시 기존 퀴즈와 최고 점수를 불러오고(Load), 퀴즈 추가 및 점수 경신 시 실시간으로 저장(Save)합니다.
인코딩: UTF-8
스키마 구조:
{
    "quizzes": [
        {
            "question": "Python에서 함수를 정의할 때 사용하는 키워드는?",
            "choices": [
                "func",
                "define",
                "def",
                "lambda"
            ],
            "answer": 3
        },
        {
            "question": "다음 중 수정이 불가능한(immutable) 파이썬 자료형은?",
            "choices": [
                "list",
                "dict",
                "tuple",
                "set"
            ],
            "answer": 3
        },
        {
            "question": "Git에서 현재 작업 중인 파일의 변경 상태를 확인하는 명령어는?",
            "choices": [
                "git status",
                "git commit",
                "git push",
                "git init"
            ],
            "answer": 1
        },
        {
            "question": "파이썬 코드를 실행할 때 터미널에 입력하는 기본 명령어 형식은?",
            "choices": [
                "run script.py",
                "python3 script.py",
                "start script.py",
                "exec script.py"
            ],
            "answer": 2
        },
        {
            "question": "Git 원격 저장소의 최신 코드를 로컬로 가져와 병합하는 명령어는?",
            "choices": [
                "git clone",
                "git push",
                "git pull",
                "git fetch"
            ],
            "answer": 3
        }
    ],
    "best_score": 3
}

-브랜치 활용 및 기능 구현
> 브랜치 생성 및 이동
root@DESKTOP-V60E01R:/mnt/c/Users/USER/Desktop/mission2#git checkout -b feature/game-logic

>game.py 기본 골격 작성
root@DESKTOP-V60E01R:/mnt/c/Users/USER/Desktop/mission2#git add game.py
root@DESKTOP-V60E01R:/mnt/c/Users/USER/Desktop/mission2#git commit -m "Feat: QuizGame 클래스 기본 구조 및 파일 입출력 구현"

>예외 처리 기능 추가
root@DESKTOP-V60E01R:/mnt/c/Users/USER/Desktop/mission2#git add game.py
root@DESKTOP-V60E01R:/mnt/c/Users/USER/Desktop/mission2#git commit -m "Refactor: 공통 입력 및 예외 처리(공백, 범위, 에러) 구현"

>퀴즈 풀기 기능 추가
root@DESKTOP-V60E01R:/mnt/c/Users/USER/Desktop/mission2#git add game.py
root@DESKTOP-V60E01R:/mnt/c/Users/USER/Desktop/mission2#git commit -m "Feat: 퀴즈 풀기 및 점수 갱신 로직 구현"

>main 브랜치로 병합
root@DESKTOP-V60E01R:/mnt/c/Users/USER/Desktop/mission2#git checkout main
root@DESKTOP-V60E01R:/mnt/c/Users/USER/Desktop/mission2#git merge feature/game-logic
root@DESKTOP-V60E01R:/mnt/c/Users/USER/Desktop/mission2#git commit -m "Merge: feature/game-logic 브랜치를 main에 병합"

-Clone & Pull 실습 수행
# 1. 다른 폴더(예: 바탕화면 등)로 이동하여 저장소 Clone 실습
root@DESKTOP-V60E01R:/mnt/c/Users/USER/Desktop/mission2# cd /mnt/c/Users/USER/Desktop
root@DESKTOP-V60E01R:/mnt/c/Users/USER/Desktop# git clone https://github.com/cjh82062954-eng/code clone_test
Cloning into 'clone_test'...
remote: Enumerating objects: 75, done.
remote: Counting objects: 100% (75/75), done.
remote: Compressing objects: 100% (56/56), done.
remote: Total 75 (delta 17), reused 47 (delta 7), pack-reused 0 (from 0)
Unpacking objects: 100% (75/75), done.
root@DESKTOP-V60E01R:/mnt/c/Users/USER/Desktop# cd clone_test

# 2. 복제된 곳에서 간단한 수정 후 커밋 및 푸시
root@DESKTOP-V60E01R:/mnt/c/Users/USER/Desktop/clone_test# echo '<!-- test -->' >> README.md
root@DESKTOP-V60E01R:/mnt/c/Users/USER/Desktop/clone_test# git add README.md
root@DESKTOP-V60E01R:/mnt/c/Users/USER/Desktop/clone_test# git commit -m "Chore: clone 디렉토리에서 README 수정"
[main b2cbba8] Chore: clone 디렉토리에서 README 수정
 1 file changed, 1 insertion(+)
root@DESKTOP-V60E01R:/mnt/c/Users/USER/Desktop/clone_test# git push origin main
Counting objects: 3, done.
Delta compression using up to 12 threads.
Compressing objects: 100% (2/2), done.
Writing objects: 100% (3/3), 322 bytes | 53.00 KiB/s, done.
Total 3 (delta 1), reused 0 (delta 0)
remote: Resolving deltas: 100% (1/1), completed with 1 local object.
To https://github.com/cjh82062954-eng/code
   fb92b46..b2cbba8  main -> main

# 3. 기존 작업 디렉토리로 돌아와서 Pull 실습
root@DESKTOP-V60E01R:/mnt/c/Users/USER/Desktop/clone_test# cd /mnt/c/Users/USER/Desktop/mission2
root@DESKTOP-V60E01R:/mnt/c/Users/USER/Desktop/mission2# git pull origin main
remote: Enumerating objects: 5, done.
remote: Counting objects: 100% (5/5), done.
remote: Compressing objects: 100% (1/1), done.
remote: Total 3 (delta 1), reused 3 (delta 1), pack-reused 0 (from 0)
Unpacking objects: 100% (3/3), done.
From https://github.com/cjh82062954-eng/code
 * branch            main       -> FETCH_HEAD
   fb92b46..b2cbba8  main       -> origin/main
Updating fb92b46..b2cbba8
Fast-forward
 README.md | 1 +
 1 file changed, 1 insertion(+)














 
