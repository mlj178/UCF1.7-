using System;
using System.Collections;
using UnityEngine;
using UnityEngine.UI;

public class HUD_TabScoreBoard : Singleton<HUD_TabScoreBoard>
{
	[SerializeField]
	private RectTransform rect;

	[SerializeField]
	private Image[] images;

	[SerializeField]
	private Vector2 showStartPos;

	[SerializeField]
	private Vector2 showEndPos;

	[SerializeField]
	protected RankField rankField;

	[SerializeField]
	protected RectTransform revengeSignRect;

	protected static readonly Vector2 revengeSignLocalPos;

	[SerializeField]
	private RectTransform myPlayerBG;

	protected TabScoreBoard_PlayerData myPlayerData;

	[SerializeField]
	private Text fpsText;

	private int passFrame;

	private float passTime;

	[SerializeField]
	private int dataInterval;

	public static Action AceUpdateAction;

	private static readonly Vector2 myPlayerBGlocalPos;

	protected override void Awake()
	{
	}

	protected virtual void Update()
	{
	}

	protected override void OnDestroy()
	{
	}

	public override void SetVisible(bool newVisible)
	{
	}

	private void NewPlayerJoin(Player newPlayer)
	{
	}

	protected virtual void OnMyPlayerJoin(Player myPlayer)
	{
	}

	private void UpdateRevengeTarget(Player target)
	{
	}

	protected virtual RankField GetEnemyRankField()
	{
		return null;
	}

	protected virtual TabScoreBoard_PlayerData AddPlayerToRankField(Player newPlayer)
	{
		return null;
	}

	private IEnumerator FPSCalculator()
	{
		return null;
	}
}
