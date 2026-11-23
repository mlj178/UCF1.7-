namespace BotAction.Skill
{
	public class Invincible : BotSkillBase
	{
		public Invincible(Bot bot, SkillKey skillKey)
			: base(null, SkillKey.F)
		{
		}

		public override bool CanDo()
		{
			return false;
		}
	}
}
