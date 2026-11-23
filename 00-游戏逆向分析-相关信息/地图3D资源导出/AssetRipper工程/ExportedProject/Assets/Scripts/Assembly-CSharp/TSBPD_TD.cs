using UnityEngine;
using UnityEngine.UI;

public class TSBPD_TD : TabScoreBoard_PlayerData
{
	[SerializeField]
	private Text kill;

	[SerializeField]
	private Text death;

	[SerializeField]
	private Image aceSign;

	[SerializeField]
	private GameObject deadSign;

	public override void Bind(Player player)
	{
	}

	protected override void SetAllTextColor(Color color)
	{
	}

	protected override Color GetColor(bool dead)
	{
		return default;
	}

	private void UpdateKill(int oldValue, int newValue)
	{
	}

	private void UpdateDeath(int oldValue, int newValue)
	{
	}

	protected override void UpdateLifeState(bool alive)
	{
	}

	private void UpdateAceSign(HUD_Role.AceSign oldSign, HUD_Role.AceSign newSign)
	{
	}
}
