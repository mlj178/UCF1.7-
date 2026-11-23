namespace BotAction.Skill
{
	public abstract class BotSkillBase : BotActionBase
	{
		protected SkillKey skillKey;

		protected float nextCheckTime;

		protected BotSkillBase(Bot bot, SkillKey skillKey)
			: base(null)
		{
		}

		public override void DoAction()
		{
		}

		protected void AddNextCheckTime(float min, float max)
		{
		}
	}
}
