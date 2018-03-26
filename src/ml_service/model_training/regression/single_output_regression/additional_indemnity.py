class AdditionalIndemnity:
    ANNUAL_INTEREST_RATE = 0.18

    def __init__(self):
        pass

    def predict(self, monthly_rent, months):
        """
        Le taux d’intérêt sur les créances de l’État, déterminé conformément à l’article 28R2 du
        Règlement sur l’administration fiscale (chapitre A-6.002, r. 1), pour le trimestre débutant
        le 1er octobre 2017 et se terminant le 31 décembre 2017, est de 6%. (2017) 149 G.O. 1, 1039.

        The interest rate is compounded for every trimester at a rate of 6% or 18% per year.
        Below is the formula to find the difference between compounded amount - original amount.

        A = P(1 + r/n)^(nt)

        A = amount
        P = payment owed
        r = annual interest rate
        n = compound interval
        t = time in years

        :param monthly_rent:
        :param months:
        :return:
        """
        n = int(months / 3) + 1
        t = months / 12.0
        nt = n * t
        PMT = monthly_rent * 4
        try:
            amount = PMT * ((1 + (self.ANNUAL_INTEREST_RATE / n))** nt)
        except ZeroDivisionError:
            return 0
        return amount - PMT
