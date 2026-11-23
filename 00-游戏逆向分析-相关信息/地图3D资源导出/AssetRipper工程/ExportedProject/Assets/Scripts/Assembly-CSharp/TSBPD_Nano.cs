using UnityEngine;
using UnityEngine.UI;

public class TSBPD_Nano : TabScoreBoard_PlayerData
{
	[SerializeField]
	private RawImage roleIcon;

	[SerializeField]
	protected Text kill;

	[SerializeField]
	private Text survival;

	public override void Bind(Player player)
	{
	}

	protected virtual void AddKillListener(PlayerData playerData)
	{
	}

	protected override void SetAllTextColor(Color color)
	{
	}

	private void OnStartRespawn(Player player)
	{
	}

	private void OnRespawn(Player player)
	{
	}

	private void UpdateNanoRoleIcon(NanoRole oldRole, NanoRole newRole)
	{
	}

	private void SetRoleIcon(NanoRole nanoRole)
	{
	}

	protected void UpdateKill(int oldValue, int newValue)
	{
	}

	private void UpdateSurvival(int oldValue, int newValue)
	{
	}

	protected override Color GetColor(bool dead)
	{
		return default;
	}

	public override int Compare(TabScoreBoard_PlayerData other)
	{
		return 0;
	}
}
