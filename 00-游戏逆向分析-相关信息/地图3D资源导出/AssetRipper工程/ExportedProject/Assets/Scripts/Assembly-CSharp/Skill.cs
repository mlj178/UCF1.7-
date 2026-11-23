using System;
using BotAction.Skill;

public abstract class Skill
{
	public string name;

	public HUD_SkillBtn skillBtn;

	public bool disabled;

	public Func<Bot, BotSkillBase> SkillAI_Creator;

	public Action Remove_Listener;

	public Skill(string name)
	{
	}

	public abstract bool TryUse(Player player);

	public abstract int GetSpriteIndex();

	public abstract void OnPlayerReSpawn();

	public abstract void OnSetOnPlayer(Player player);

	public virtual void OnRemoveFromPlayer(Player player)
	{
	}

	public bool TryGetSkillAI(Bot bot, out BotSkillBase skillAI)
	{
		skillAI = null;
		return false;
	}
}
