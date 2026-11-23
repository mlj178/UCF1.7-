using System;
using UnityEngine;
using UnityEngine.UI;

public class TabScoreBoard_PlayerData : RecyclableObject
{
	protected static readonly Color color_MyDead;

	protected static readonly Color color_Teammate;

	protected static readonly Color color_Enemy;

	protected static readonly Color color_OtherDead;

	protected static readonly Color color_Me_DM;

	protected static readonly Color color_Other_DM;

	protected static readonly Color color_Vip;

	protected static readonly Color color_Vip_Dead;

	[SerializeField]
	private RectTransform rect;

	[SerializeField]
	private RawImage vipIcon;

	[SerializeField]
	private RawImage levelIcon;

	[SerializeField]
	private Text playerName;

	[SerializeField]
	private Text ping;

	[SerializeField]
	private GameObject vvipSign;

	public Action<TabScoreBoard_PlayerData> rerankAction;

	public static int DataInterval;

	public int currentRank
	{
		get
		{
			return 0;
		}
		set
		{
		}
	}

	public Player player { get; private set; }

	public virtual void Bind(Player player)
	{
	}

	public virtual void SetRank(int rank)
	{
	}

	protected virtual Color GetColor(bool dead)
	{
		return default;
	}

	protected virtual void SetAllTextColor(Color color)
	{
	}

	protected virtual void UpdateLifeState(bool alive)
	{
	}

	public virtual int Compare(TabScoreBoard_PlayerData other)
	{
		return 0;
	}

	public static int KillAndDeathCompare(Player p1, Player p2)
	{
		return 0;
	}
}
