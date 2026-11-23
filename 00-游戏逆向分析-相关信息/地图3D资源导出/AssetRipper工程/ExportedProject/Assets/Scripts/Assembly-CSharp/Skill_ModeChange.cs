using System;

public class Skill_ModeChange : Skill
{
	private Func<bool> getModeState;

	private Func<bool> changeModeFunc;

	public Skill_ModeChange(string name, Func<bool> getModeState, Func<bool> changeModeFunc)
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

	public override void OnPlayerReSpawn()
	{
	}

	public override void OnSetOnPlayer(Player player)
	{
	}
}
