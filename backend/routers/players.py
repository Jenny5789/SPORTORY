from fastapi import APIRouter, HTTPException, Query

from backend.database import get_connection


router = APIRouter(
    prefix="/players",
    tags=["Players"]
)


@router.get("")
def get_players():
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
               SELECT
                p.player_id,
                p.first_name,
                p.last_name,
                p.nationality,
                p.birth_date,
                p.height_cm,
                p.play_hand,
                pi.image_path,
                r.singles_rank
            FROM players p
            LEFT JOIN player_images pi
                ON p.player_id = pi.player_id
            LEFT JOIN LATERAL (
                SELECT singles_rank
                FROM player_ranking_history
                WHERE player_id = p.player_id
                ORDER BY rank_date DESC
                LIMIT 1
            ) r ON TRUE
            ORDER BY r.singles_rank ASC NULLS LAST
                """
            )

            rows = cursor.fetchall()

    finally:
        connection.close()

    players = []

    for row in rows:
        image_url = None

        if row[7]:
            image_url = row[7]

        players.append(
            {
                "player_id": row[0],
                "first_name": row[1],
                "last_name": row[2],
                "nationality": row[3],
                "birth_date": row[4],
                "height_cm": row[5],
                "play_hand": row[6],
                "image_url": image_url
            }
        )

    return players

@router.get("/{player_id}/bio")
def get_player_bio(player_id: str):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    section,
                    item_order,
                    original_text,
                    translated_text
                FROM player_bios
                WHERE player_id = %s
                ORDER BY
                    CASE
                        WHEN section = 'personal' THEN 1
                        WHEN section = 'career' THEN 2
                        ELSE 3
                    END,
                    item_order
                """,
                (player_id,)
            )

            rows = cursor.fetchall()

    finally:
        connection.close()

    if not rows:
        raise HTTPException(
            status_code=404,
            detail="Player bio not found"
        )

    bio = {
        "personal": [],
        "career": []
    }

    for row in rows:
        section = row[0]

        item = {
            "item_order": row[1],
            "original_text": row[2],
            "translated_text": row[3]
        }

        if section in bio:
            bio[section].append(item)

    return bio

@router.get("/{player_id}")
def get_player(player_id: str):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    p.player_id,
                    p.first_name,
                    p.last_name,
                    p.nationality,
                    p.birth_date,
                    p.height_cm,
                    p.weight_kg,
                    p.play_hand,
                    p.backhand,
                    p.pro_year,
                    pi.image_path
                FROM players p
                LEFT JOIN player_images pi
                    ON p.player_id = pi.player_id
                WHERE p.player_id = %s
                """,
                (player_id,)
            )

            row = cursor.fetchone()

    finally:
        connection.close()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Player not found"
        )

    image_url = None

    if row[10]:
        image_url = row[10]

    return {
        "player_id": row[0],
        "first_name": row[1],
        "last_name": row[2],
        "nationality": row[3],
        "birth_date": row[4],
        "height_cm": row[5],
        "weight_kg": row[6],
        "play_hand": row[7],
        "backhand": row[8],
        "pro_year": row[9],
        "image_url": image_url
    }


@router.get("/{player_id}/rankings")
def get_player_rankings(
    player_id: str,
    limit: int = Query(default=10, ge=1, le=100)
    ):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    rank_date,
                    singles_rank,
                    singles_points,
                    race_rank,
                    race_points,
                    doubles_rank,
                    doubles_points
                FROM player_ranking_history
                WHERE player_id = %s
                ORDER BY rank_date DESC
                LIMIT %s
                """,
                (player_id,limit)
            )

            rows = cursor.fetchall()

    finally:
        connection.close()

    if not rows:
        raise HTTPException(
            status_code=404,
            detail="Ranking history not found"
        )

    rankings = []

    for row in rows:
        rankings.append(
            {
                "rank_date": row[0],
                "singles_rank": row[1],
                "singles_points": row[2],
                "race_rank": row[3],
                "race_points": row[4],
                "doubles_rank": row[5],
                "doubles_points": row[6]
            }
        )

    return rankings

@router.get("/{player_id}/stats")
def get_player_stats(player_id: str):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    category,
                    surface,
                    event_year,
                    rank_date,
                    aces,
                    double_faults,
                    first_serve_percentage,
                    first_serve_points_won_percentage,
                    second_serve_points_won_percentage,
                    break_points_faced,
                    break_points_saved_percentage,
                    service_games_played,
                    service_games_won_percentage,
                    service_points_won_percentage,
                    first_serve_return_points_won_percentage,
                    second_serve_return_points_won_percentage,
                    break_points_opportunities,
                    break_points_converted_percentage,
                    return_games_played,
                    return_games_won_percentage,
                    return_points_won_percentage,
                    total_points_won_percentage
                FROM player_stats
                WHERE player_id = %s
                ORDER BY event_year DESC NULLS LAST, category, surface
                """,
                (player_id,)
            )

            rows = cursor.fetchall()

    finally:
        connection.close()

    if not rows:
        raise HTTPException(
            status_code=404,
            detail="Player stats not found"
        )

    stats = []

    for row in rows:
        stats.append(
            {
                "category": row[0],
                "surface": row[1],
                "event_year": row[2],
                "rank_date": row[3],
                "aces": row[4],
                "double_faults": row[5],
                "first_serve_percentage": row[6],
                "first_serve_points_won_percentage": row[7],
                "second_serve_points_won_percentage": row[8],
                "break_points_faced": row[9],
                "break_points_saved_percentage": row[10],
                "service_games_played": row[11],
                "service_games_won_percentage": row[12],
                "service_points_won_percentage": row[13],
                "first_serve_return_points_won_percentage": row[14],
                "second_serve_return_points_won_percentage": row[15],
                "break_points_opportunities": row[16],
                "break_points_converted_percentage": row[17],
                "return_games_played": row[18],
                "return_games_won_percentage": row[19],
                "return_points_won_percentage": row[20],
                "total_points_won_percentage": row[21]
            }
        )

    return stats

@router.get("/{player_id}/matches")
def get_player_matches(
    player_id: str,
    limit: int = Query(default=10, ge=1, le=100)
):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    m.source_match_id,
                    m.round_id,
                    m.round_name,
                    m.win_loss,
                    m.opponent_id,
                    m.opponent_first_name,
                    m.opponent_last_name,
                    m.opponent_nationality_code,
                    m.opponent_rank,
                    m.set1_player,
                    m.set1_opponent,
                    m.set1_tiebreak,
                    m.set2_player,
                    m.set2_opponent,
                    m.set2_tiebreak,
                    m.set3_player,
                    m.set3_opponent,
                    m.set4_player,
                    m.set4_opponent,
                    t.name,
                    t.country,
                    t.city,
                    t.start_date,
                    t.end_date,
                    t.event_type,
                    t.surface,
                    t.indoor_outdoor
                FROM matches m
                JOIN tournaments t
                    ON m.tournament_id = t.tournament_id
                WHERE m.player_id = %s
                ORDER BY t.start_date DESC, m.round_id::INTEGER DESC
                LIMIT %s
                """,
                (player_id, limit)
            )

            rows = cursor.fetchall()

    finally:
        connection.close()

    if not rows:
        raise HTTPException(
            status_code=404,
            detail="Player matches not found"
        )

    matches = []

    for row in rows:
        matches.append(
            {
                "source_match_id": row[0],
                "round_id": row[1],
                "round_name": row[2],
                "win_loss": row[3],
                "opponent": {
                    "player_id": row[4],
                    "first_name": row[5],
                    "last_name": row[6],
                    "nationality_code": row[7],
                    "rank": row[8]
                },
                "score": {
                    "set1": {
                        "player": row[9],
                        "opponent": row[10],
                        "tiebreak": row[11]
                    },
                    "set2": {
                        "player": row[12],
                        "opponent": row[13],
                        "tiebreak": row[14]
                    },
                    "set3": {
                        "player": row[15],
                        "opponent": row[16]
                    },
                    "set4": {
                        "player": row[17],
                        "opponent": row[18]
                    }
                },
                "tournament": {
                    "name": row[19],
                    "country": row[20],
                    "city": row[21],
                    "start_date": row[22],
                    "end_date": row[23],
                    "event_type": row[24],
                    "surface": row[25],
                    "indoor_outdoor": row[26]
                }
            }
        )

    return matches