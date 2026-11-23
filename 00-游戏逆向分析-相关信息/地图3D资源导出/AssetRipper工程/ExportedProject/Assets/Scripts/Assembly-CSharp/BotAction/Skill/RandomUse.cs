namespace BotAction.Skill
{
	public class RandomUse : BotSkillBase
	{
		private float minCheckTime;

		private float maxCheckTime;

		public RandomUse(Bot bot, SkillKey skillKey, float min, float max)
			: base(null, SkillKey.F)
		{
		}

		public override bool CanDo()
		{
			return false;
		}
	}
}
