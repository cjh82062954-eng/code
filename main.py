from game import QuizGame

if __name__ == "__main__":
    try:
        game = QuizGame()
        game.run()
    except (KeyboardInterrupt, EOFError):
        print("\n\n⚠️ 비정상적인 입력이 감지되었습니다. 안전하게 프로그램을 종료합니다.")