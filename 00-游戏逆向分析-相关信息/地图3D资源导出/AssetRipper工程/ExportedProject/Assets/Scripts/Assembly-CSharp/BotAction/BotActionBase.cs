namespace BotAction
{
	public abstract class BotActionBase
	{
		protected Bot bot;

		protected Player player => null;

		public bool isFinished { get; protected set; }

		protected BotActionBase(Bot bot)
		{
		}

		public abstract bool CanDo();

		public abstract void DoAction();

		public virtual void Update()
		{
		}

		public void Finish()
		{
		}

		protected virtual void OnActionFinish()
		{
		}
	}
}
