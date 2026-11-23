using UnityEngine;
using UnityEngine.UI;

public class HUD_TabScoreBoard_TD : HUD_TabScoreBoard
{
	[SerializeField]
	private RankField enemyRankField;

	[SerializeField]
	private Image[] scoreboardImages;

	[SerializeField]
	private Sprite[] scoreboardSprs;

	[SerializeField]
	private Sprite[] aceSignSprs;

	[SerializeField]
	private GameObject firstIcon;

	protected override void Update()
	{
	}

	protected override void OnMyPlayerJoin(Player myPlayer)
	{
	}

	protected override TabScoreBoard_PlayerData AddPlayerToRankField(Player newPlayer)
	{
		return null;
	}

	protected override RankField GetEnemyRankField()
	{
		return null;
	}

	public static Sprite GetAceSign(HUD_Role.AceSign sign)
	{
		return null;
	}
}
