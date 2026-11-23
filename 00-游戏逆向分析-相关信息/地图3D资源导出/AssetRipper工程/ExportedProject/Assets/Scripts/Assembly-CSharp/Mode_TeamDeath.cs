using UnityEngine;

public class Mode_TeamDeath : ModeBase
{
	[SerializeField]
	private AudioClip remain10KillSound;

	[SerializeField]
	private CommonHud_1 remain10KillTip;

	[SerializeField]
	private GameObject invinsibleGauge;

	private bool firstKill;

	private bool lastKill_BL;

	private bool lastKill_GR;

	protected override void Start()
	{
	}

	protected override void OnMyPlayerJoin(Player myPlayer)
	{
	}

	private void DeathEvent(DeathEventData eventData)
	{
	}

	private SpecialKillType FirstAndLastKillCheck(Entity killer, Entity dead)
	{
		return SpecialKillType.None;
	}

	private void GameOver()
	{
	}

	protected override void OnScoreReachTarget(bool left)
	{
	}

	protected override void OnTimeOut()
	{
	}

	private void Show10KillTip()
	{
	}
}
