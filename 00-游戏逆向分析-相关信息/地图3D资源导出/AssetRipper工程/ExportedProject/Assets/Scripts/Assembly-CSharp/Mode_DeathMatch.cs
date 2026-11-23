using UnityEngine;

public class Mode_DeathMatch : ModeBase
{
	private bool firstKill;

	[SerializeField]
	private GameObject invinsibleGauge;

	protected override void Update()
	{
	}

	protected override void Start()
	{
	}

	protected override void OnMyPlayerJoin(Player myPlayer)
	{
	}

	private void OnMyKillChange(int oldKill, int newKill)
	{
	}

	private void DeathEvent(DeathEventData eventData)
	{
	}

	protected override void OnTimeOut()
	{
	}

	private void GameOver()
	{
	}

	private SpecialKillType FirstAndLastKillCheck(Entity killer, Entity dead)
	{
		return SpecialKillType.None;
	}
}
