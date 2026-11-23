namespace BotAction.Skill
{
	public class SpeedUp : BotSkillBase
	{
		public SpeedUp(Bot bot, SkillKey skillKey)
			: base(null, SkillKey.F)
		{
		}

		public override bool CanDo()
		{
			return false;
		}
	}
}
