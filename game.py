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
            Quiz("파이썬 코드를 실행할 때 터미널에 입력하는 기본 명령어 형식은?", ["run script.py", "python3 script.py", "start script.py", "exec script.py"], 2),
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