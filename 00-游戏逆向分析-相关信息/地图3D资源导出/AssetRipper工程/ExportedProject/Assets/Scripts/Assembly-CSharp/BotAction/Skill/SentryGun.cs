namespace BotAction.Skill
{
	public class SentryGun : BotSkillBase
	{
		private Skill_SentryGun bindSkill;

		public SentryGun(Bot bot, SkillKey skillKey, Skill_SentryGun skill)
			: base(null, SkillKey.F)
		{
		}

		protected override void OnActionFinish()
		{
		}

		public override bool CanDo()
		{
			return false;
		}
	}
}
