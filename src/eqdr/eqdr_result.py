class EqdrResult:
    def __init__(
        self,
        solutions: "list[tuple[str, float]]",
        statistics: any,
    ) -> None:
        self.solutions: list[tuple[str, float]] = solutions
        self.statistics = statistics
