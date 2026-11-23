using UnityEngine;
using UnityEngine.UI;

public class TSBPD_DM : TabScoreBoard_PlayerData
{
	[SerializeField]
	private Text rankText;

	[SerializeField]
	private Text kill;

	[SerializeField]
	private Text death;

	protected override void SetAllTextColor(Color color)
	{
	}

	public override void Bind(Player player)
	{
	}

	private void UpdateKill(int oldValue, int newValue)
	{
	}

	private void UpdateDeath(int oldValue, int newValue)
	{
	}

	public override void SetRank(int rank)
	{
	}

	protected override Color GetColor(bool dead)
	{
		return default;
	}
}
