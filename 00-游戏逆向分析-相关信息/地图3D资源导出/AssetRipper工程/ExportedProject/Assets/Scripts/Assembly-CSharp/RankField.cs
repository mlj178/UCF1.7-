using System.Collections.Generic;
using UnityEngine;

public class RankField : MonoBehaviour
{
	[SerializeField]
	private GameObject prefab;

	private SimpleObjectPool pool;

	private List<TabScoreBoard_PlayerData> list;

	public TabScoreBoard_PlayerData AddPlayer(Player player)
	{
		return null;
	}

	public void TryRerank(TabScoreBoard_PlayerData target)
	{
	}

	public TabScoreBoard_PlayerData FindDataByPlayer(Player player)
	{
		return null;
	}

	public TabScoreBoard_PlayerData FindPlayerByRank(int rank)
	{
		return null;
	}
}
