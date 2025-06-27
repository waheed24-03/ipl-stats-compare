def get_batsman_vs_bowler_stats(df, batsman, bowler):
    duel = df[(df['batter'] == batsman) & (df['bowler'] == bowler)]

    runs = duel['batsman_runs'].sum()
    balls = duel.shape[0]
    outs = duel[duel['player_dismissed'] == batsman].shape[0]
    strike_rate = (runs / balls) * 100 if balls else 0
    average = (runs / outs) if outs else runs
    fours = duel[duel['batsman_runs'] == 4].shape[0]
    sixes = duel[duel['batsman_runs'] == 6].shape[0]

    # Fixed dominance logic
    if balls == 0:
        dominance = 50
    else:
        batsman_score = (runs * 1.5 + fours + sixes * 2) - outs * 10
        bowler_score = outs * 12 + (balls - runs)
        total_score = batsman_score + bowler_score
        dominance = round((batsman_score / total_score) * 100, 2) if total_score > 0 else 50

    return {
        "Runs": runs,
        "Balls Faced": balls,
        "Outs": outs,
        "Strike Rate": round(strike_rate, 2),
        "Fours": fours,
        "Sixes": sixes,
        "Average": round(average, 2),
        "Batsman Dominance %": dominance
    }
