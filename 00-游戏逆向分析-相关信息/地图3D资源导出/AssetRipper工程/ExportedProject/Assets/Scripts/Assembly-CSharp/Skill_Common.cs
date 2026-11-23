using System;

public class Skill_Common : Skill
{
	private float coldFinishTime;

	private Func<Player, bool> work;

	private float coldTime;

	private bool isColdFinish => false;

	public bool isCanUse => false;

	public Skill_Common(string name, Func<Player, bool> workFunction, float coldTime)
		: base(null)
	{
	}

	public override int GetSpriteIndex()
	{
		return 0;
	}

	public override bool TryUse(Player player)
	{
		return false;
	}

	protected bool BasicCheck()
	{
		return false;
	}

	public override void OnPlayerReSpawn()
	{
	}

	public override void OnSetOnPlayer(Player player)
	{
	}

	public void StartCold()
	{
	}

	public void EndCold()
	{
	}
}
